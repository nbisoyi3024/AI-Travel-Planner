from rag.tools import cached_places
from rag.rag import query_rag

# MCP Tool for Places API
def places_mcp_tool(query):

    results = cached_places(query)

    return {
        "tool": "places_tool",
        "results": results
    }

#RAG MCP Tool
def rag_mcp_tool(query):

    results = query_rag(query)

    return {
        "tool": "rag_tool",
        "results": results
    }