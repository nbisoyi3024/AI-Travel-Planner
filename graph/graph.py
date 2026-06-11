#Workflow graph 
from langgraph.graph import StateGraph, END

from agents.agents import (
    supervisor_agent,
    planner_agent,
    places_agent,
    rag_agent
    )

def build_graph():
    # Create a state graph
    workflow = StateGraph(dict)
    
    #add agents as nodes
    workflow.add_node("supervisor", supervisor_agent)

    workflow.add_node("planner", planner_agent)
    workflow.add_node("places", places_agent)
    workflow.add_node("rag", rag_agent)
    
    #starting point for the graph
    workflow.set_entry_point("supervisor")
    
    #routing logic
    def route(state):
        return state.get("next","rag")
    
    #dynamic routing based on supervisor output
    workflow.add_conditional_edges(
        "supervisor",
        route,
        {
            "planner": "planner",
            "places": "places",
            "rag": "rag"
        }
    )
    #end execution
    workflow.add_edge("planner", END)
    workflow.add_edge("places", END)
    workflow.add_edge("rag", END)

    return workflow.compile()