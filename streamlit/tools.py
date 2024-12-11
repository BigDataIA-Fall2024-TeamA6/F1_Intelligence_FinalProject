from langchain_core.tools import tool
from serpapi import GoogleSearch
from pinecone import Pinecone,ServerlessSpec
from langchain_core.agents import AgentAction
from sentence_transformers import SentenceTransformer
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
import streamlit as st
from state import State,QueryOutput
from langchain import hub
from db import get_connection
import time
import os
from dotenv import load_dotenv



load_dotenv()

db = get_connection()

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",api_key=api_key)
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
assert len(query_prompt_template.messages) == 1

pc_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key = pc_api_key)
spec = ServerlessSpec(cloud = "aws", region = "us-east-1")



def write_query(state: State):
    """Generate SQL query to fetch information."""
    prompt = query_prompt_template.invoke(
        {
            "dialect": db.dialect,
            "top_k": 5,
            "table_info": db.get_table_info(table_names=["validation_table"]),
            "input": state["question"],
        }
    )
    structured_llm = llm.with_structured_output(QueryOutput)
    result = structured_llm.invoke(prompt)
    return {"query": result["query"]}

def execute_query(state: State):
    """Execute SQL query."""
    execute_query_tool = QuerySQLDataBaseTool(db=db)
    return {"result": execute_query_tool.invoke(state["query"])}

@tool("racepass_info")
def racepass_info(question: str):
    """Fetches the racepass details from the table using text2SQL and populates it onto the  confirmation page."""  
    
    sql_qry = write_query({"question": question})
    
    
    res = execute_query({"query": sql_qry})
        
    return res["result"]
    
    

@tool("web_search")
def web_search(query: str):
    """Finds general knowledge information using Google search. Can also be used
    to augment more 'general' knowledge to a previous specialist query."""
    serpapi_params = {
    "engine": "google",
    "api_key": os.getenv("SERP_API_KEY")
    }
    search = GoogleSearch({
        **serpapi_params,
        "q": query,
        "num": 5
    })
    results = search.get_dict()["organic_results"]
    contexts = "\n---\n".join(
        ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
    )
    return contexts


def format_rag_contexts(matches: list):
    contexts = []
    for match in matches:
        metadata = match.metadata if hasattr(match, 'metadata') else {}
        if metadata:
            text = metadata.get('text', '')
        contexts.append(text)
    context_str = "\n---\n".join(contexts)
    return context_str

def build_knowledge_base():
    index_name = "pdf-364ff30954" # insert PDF document name here

    # check if index already exists (it shouldn't if this is first time)
    if index_name not in pc.list_indexes().names():
    # if does not exist, create index
        pc.create_index(
        index_name,
        dimension=1536,  # dimensionality of embed 3
        metric='dotproduct',
        spec=spec
    )
    # wait for index to be initialized
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
        
    # connect to index
    index = pc.Index(index_name)
    return index    


@tool("rag_search")
def rag_search(query: str):
    """Finds specialist information on AI using a natural language query."""
    encoder = SentenceTransformer("all-mpnet-base-v2")    
    index = build_knowledge_base()
    query_em = encoder.encode(query).tolist()
    results = index.query(vector=query_em, top_k=2, include_metadata=True)
    context_str = format_rag_contexts(results.matches)
    return context_str



@tool("final_answer")
def final_answer(
    introduction: str,
    research_steps: str,
    main_body: str,
    conclusion: str,
    sources: str
):
    """Returns a natural language response to the user in the form of a research
    report. There are several sections to this report, those are:
    - `introduction`: a short paragraph introducing the user's question and the
    topic we are researching.
    - `research_steps`: a few bullet points explaining the steps that were taken
    to research your report.
    - `main_body`: this is where the bulk of high quality and concise
    information that answers the user's question belongs. It is 3-4 paragraphs
    long in length.
    - `conclusion`: this is a short single paragraph conclusion providing a
    concise but sophisticated view on what was found.
    - `sources`: a bulletpoint list provided detailed sources for all information
    referenced during the research process
    """
    print("final_answer")
    if type(research_steps) is list:
        research_steps = "\n".join([f"- {r}" for r in research_steps])
    if type(sources) is list:
        sources = "\n".join([f"- {s}" for s in sources])
    return ""

from langchain_core.prompts import ChatPromptTemplate

# system_prompt = """
# You are the F1-AI, the AI decision maker. You're designed to invoke a tool from the list of tools provided to you 
# based on the user's request in the prompt.
# Given the user's query you must use and redirect to the appropriate tool based on the
# list of tools provided to you. Do not hallucinate or recursively call a tool multiple times.
# Use only a SINGLE tool based on the query based on the user prompt. Do NOT use multiple tools.
# Once the tool has been called, TERMINATE. Do NOT call the same tool recursively.
# """
system_prompt = """
You are an advanced Agentic AI responsible for providing an optimal and seamless user experience for the Formula 1 website.
Your primary goal is to understand the user's prompt, analyze the context, and correctly invoke a tool from 
the list of tools available to you.
Once a tool is invoked, you will return the result directly.
You must not recursively invoke the same tool or any other tool once an invocation is made. """

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", "{input}"),
    # ("assistant", "scratchpad: {scratchpad}"),
])

"""Next, we must initialize our `llm` (for this we use `gpt-4o`) and then create the _runnable_ pipeline of our Oracle.

The runnable connects our inputs (the user `input` and `chat_history`) to our `prompt`, and our `prompt` to our `llm`. It is also where we _bind_ our tools to the LLM and enforce function calling via `tool_choice="any"`.
"""

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.environ["OPENAI_API_KEY"],
    temperature=0
)

tools=[
    rag_search,
    racepass_info,
    final_answer
]


oracle = (
    {
        "input": lambda x: x["input"]
    }
    | prompt
    | llm.bind_tools(tools, tool_choice="any")
)

def run_oracle(state: list):
    print("run_oracle")
    print(f"intermediate_steps: {state['intermediate_steps']}")
    out = oracle.invoke(state)
    tool_name = out.tool_calls[0]["name"]
    tool_args = out.tool_calls[0]["args"]
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log="TBD"
    )
    return {
        "intermediate_steps": [action_out]
    }
    
tool_str_to_func = {
    "rag_search": rag_search,
    "racepass_info": racepass_info,
    "final_answer": final_answer
}
    

def run_tool(state: list):
    # use this as helper function so we repeat less code
    tool_name = state["intermediate_steps"][-1].tool
    tool_args = state["intermediate_steps"][-1].tool_input
    print(f"{tool_name}.invoke(input={tool_args})")
    # run tool
    out = tool_str_to_func[tool_name].invoke(input=tool_args)
    action_out = AgentAction(
        tool=tool_name,
        tool_input=tool_args,
        log=str(out)
    )
    return {"intermediate_steps": [action_out]}