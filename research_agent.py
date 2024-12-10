import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from tools import run_oracle,run_tool
from state import AgentState

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

encoder = SentenceTransformer("all-mpnet-base-v2")


def router(state: list):
    # return the tool name to use
    if isinstance(state["intermediate_steps"], list):
        return state["intermediate_steps"][-1].tool
    else:
        # if we output bad format go to final answer
        print("Router invalid format")
        return "final_answer"
 


from langgraph.graph import StateGraph, END

def get_graph():
    graph = StateGraph(AgentState)

    graph.add_node("oracle", run_oracle)
    graph.add_node("rag_search", run_tool)
    graph.add_node("racepass_info", run_tool)
    graph.add_node("final_answer", run_tool)

    graph.set_entry_point("oracle")

    graph.add_conditional_edges(
        source="oracle",  # where in graph to start
        path=router,  # function to determine which node is called
    )


    # if anything goes to final answer, it must then move to END
    graph.add_edge("oracle", "final_answer")
    graph.add_edge("final_answer", END)

    ai_graph = graph.compile()
    
    return ai_graph


runnable = get_graph()
