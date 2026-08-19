# ReAct agent - reasons and acts dynamically instead of fixed routing
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from tools.mcp_tools import rag_mcp_tool, places_mcp_tool

llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def search_places(query: str) -> str:
    """Search for real places like restaurants, hotels, attractions.
    Use this when user asks about specific places in a city."""
    
    result = places_mcp_tool(query)
    places = result.get("results", [])
    
    if not places:
        return "No places found."
    
    return "\n".join([
        f"{p.get('name')} - Rating: {p.get('rating')} - {p.get('address')}"
        for p in places if isinstance(p, dict)
    ])

@tool
def search_knowledge_base(query: str) -> str:
    """Search travel knowledge base for general travel tips and information.
    Use this for general travel questions."""
    
    result = rag_mcp_tool(query)
    
    if isinstance(result, dict):
        return result.get("results", "No results found.")
    return str(result)

tools = [search_places, search_knowledge_base]

react_agent_executor = create_agent(llm, tools)