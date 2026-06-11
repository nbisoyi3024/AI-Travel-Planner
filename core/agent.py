#main brain/Orchestrator for the multi-agent system. 
from graph.graph import build_graph
# future use

graph = build_graph()


# ---------------- WRAPPER AGENT ----------------
def run_agent(user_input, session_id):

    state = {
        "input": user_input,
        "session_id": session_id,
        "steps": []
    }

    result = graph.invoke(state)

    return {
        "answer": result.get("answer", ""),
        "source": result.get("source", "unknown")
    }


