#Logic for multiple agents: supervisor, planner, places, RAG

from langchain_openai import ChatOpenAI

from tools.mcp_tools import rag_mcp_tool, places_mcp_tool

llm = ChatOpenAI(model="gpt-4o-mini")


# ---------------- SUPERVISOR AGENT ----------------
def supervisor_agent(state):

    query = state["input"].lower()

    places_keywords = [
        "restaurant", "food", "eat", "cafe",
        "hotel", "stay","place","cafes",
        "near", "nearby","city", "location",
        "visit", "places", "attractions",
        "things to do"
    ]

    planner_keywords = [
        "plan", "trip", "itinerary", "travel plan"
    ]

    if any(word in query for word in planner_keywords):

        return {
            **state,
            "next": "planner"
        }

    elif any(word in query for word in places_keywords):

        return {
            **state,
            "next": "places"
        }

    else:
        return {
        **state,
        "next": "rag"
        }


# ---------------- PLANNER AGENT ----------------
def planner_agent(state):

    query = state["input"]

    response = f"""
    ✈️ Travel Itinerary for: {query}

    Day 1:
    • Explore local attractions
    • Try famous restaurants

    Day 2:
    • Visit museums and cafes
    • Evening city walk
    """

    return {
        **state,
        "answer": response,
        "source": "planner_agent"
    }


# ---------------- PLACES AGENT ----------------
def places_agent(state):

    query = state["input"]

    result = places_mcp_tool(query)
    places = result.get("results",[])

    if not isinstance(places, list) or not places:

        return {
            **state,
            "answer": "No places found.",
            "source": "🤖places_agent"
        }

    context = "\n".join([
       f"{p.get('name', 'Unknown')} - {p.get('rating', 'N/A')} - {p.get('address', 'No address')}"
            for p in places if isinstance(p, dict)
        ])

    response = llm.invoke(f"""
    
    You are a travel assistant.
    Write a clean, well-formatted answer.

       RULES:
     - Start with 1 short intro sentence
     - keep tone warm and conversational
     - Then list 3–4 places using bullet points
     - Each place should have:
       • Name
       • One short highlight
     - End with 1–2 helpful tips
     - show ratings if available
     - Keep it concise and readable
     - Use emojis where appropriate (📍 ☕ 💡)
     - At the end, ask ONE short follow-up question.
    Context:
    {context}

    User query:
    {query}
    """)

    return {
        **state,
        "answer": response.content,
        "source": "🤖places_agent"
    }


# ---------------- RAG AGENT ----------------
def rag_agent(state):

    query = state["input"]

    result = rag_mcp_tool(query)

    if isinstance(result, dict):
          context = result.get("results", "")
    else:
         context = str(result)
    
    response = llm.invoke(f"""
    You are a travel assistant.

    Answer the user's question using this context.

    Context:
    {context}

    User query:
    {query}
    """)

    return {
        **state,
        "answer": response.content,
        "source": "🤖rag_agent"
    }