from langchain_core.tools import tool
from serpapi import GoogleSearch
from pinecone import Pinecone,ServerlessSpec
from langchain_core.agents import AgentAction
from sentence_transformers import SentenceTransformer
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from openai import OpenAIError, NotFoundError
import streamlit as st
from state import State,QueryOutput
from langchain import hub
from db import get_connection
import time
import os
import logging
from dotenv import load_dotenv



load_dotenv()

db = get_connection()

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini",api_key=api_key)
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")
assert len(query_prompt_template.messages) == 1

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
spec = ServerlessSpec(cloud = "aws", region = "us-east-1")

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.DEBUG, filename="research_agent_debug.log")



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


# def format_rag_contexts(matches: list):
#     contexts = []
#     for match in matches:
#         metadata = match.metadata if hasattr(match, 'metadata') else {}
#         if metadata:
#             text = metadata.get('text', '')
#         contexts.append(text)
#     context_str = "\n---\n".join(contexts)
#     return context_str

# def build_knowledge_base():
#     index_name = "pdf-364ff30954" # insert PDF document name here

#     # check if index already exists (it shouldn't if this is first time)
#     if index_name not in pc.list_indexes().names():
#     # if does not exist, create index
#         pc.create_index(
#         index_name,
#         dimension=1536,  # dimensionality of embed 3
#         metric='dotproduct',
#         spec=spec
#     )
#     # wait for index to be initialized
#     while not pc.describe_index(index_name).status['ready']:
#         time.sleep(1)
        
#     # connect to index
#     index = pc.Index(index_name)
#     return index    


@tool("rag_search")
def rag_search(query: str):
    """
    Perform a RAG (Retrieval-Augmented Generation) search using Pinecone vector database
    and then generate a final answer using an OpenAI LLM (with fallback options).

    Args:
        query (str): The user's query.
        index_name (str): The name of the Pinecone index.
        top_k (int): Number of top results to retrieve.

    Returns:
        str: The final response to the user.
    """
    index_name = "f1-data-index"
    top_k = 3

    try:
        logging.debug(f"Received query: {query}")

        # Ensure index exists
        if index_name not in [idx.name for idx in pc.list_indexes()]:
            raise ValueError(f"Index {index_name} does not exist. Please create the index before querying.")

        # Connect to the Pinecone index
        index = pc.Index(index_name)

        # Generate embeddings for the query
        query_embedding = embeddings.embed_query(query)

        # Perform similarity search
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
        )

        # Extract and format results
        contexts = []
        for match in results.matches:
            metadata = match.metadata
            text = metadata.get("text", "No metadata found")
            category = metadata.get("category", "General")
            season = metadata.get("season", "N/A")
            contexts.append(f"Category: {category}, Season: {season}\n{text}")

        context_text = "\n\n".join(contexts) if contexts else "No relevant results found."

        logging.debug(f"RAG search context: {context_text}")

        # If no relevant context, return a default message
        if not context_text.strip() or context_text.strip() == "No relevant results found.":
            return "I couldn't find relevant information for your query in the database."

        # Initialize OpenAI LLM with fallback
        try:
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.7,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
        except NotFoundError:
            try:
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.2,
                    openai_api_key=os.getenv("OPENAI_API_KEY")
                )
                logging.warning("Falling back to GPT-3.5 as GPT-4 is not available.")
            except OpenAIError as e:
                raise RuntimeError(f"Failed to initialize OpenAI language model: {str(e)}")

        # Create a prompt with the retrieved context
        prompt = f"""You are an AI assistant specialized in Formula 1 historical data.
You have access to historical data from 2013 to 2024.

Query: '{query}'

Context retrieved from the database:
{context_text}

Provide an answer to the query based on the context.

Response:"""

        # Invoke the LLM to generate the final answer
        response = llm.invoke(prompt).content
        logging.debug(f"Generated AI Response: {response}")

        return response

    except Exception as e:
        logging.error(f"Error performing RAG search and generating response: {e}")
        return f"An error occurred while processing your query: {str(e)}"


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