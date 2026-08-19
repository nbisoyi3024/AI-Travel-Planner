#Logic for multiple agents: supervisor, planner, places, RAG
import json

from langchain_openai import ChatOpenAI

from tools.mcp_tools import rag_mcp_tool, places_mcp_tool
from utils.logger import logger

llm = ChatOpenAI(model="gpt-4o-mini")

# ---------------- SUPERVISOR AGENT ----------------
def supervisor_agent(state):

    query = state["input"].lower()
    logger.info("Supervisor received travel query")
    
    planner_keywords = [
        "plan", "trip", "itinerary", "travel plan"
    ]
    restaurant_keywords = [
        "restaurant", "food", "eat", "cafe", "dining"
    ]
    hotel_keywords = [
        "hotel", "stay", "accommodation", "where to sleep"
    ]
    attraction_keywords = [
        "visit", "places", "attractions", "things to do", "sightseeing"
    ]
    budget_keywords = [
        "budget", "cost", "price", "how much", "expensive", "cheap"
    ]

    if any(word in query for word in planner_keywords):
        logger.info("Supervisor routed request to planner")
        return {**state,"next": "planner"}

    elif any(word in query for word in restaurant_keywords):
        logger.info("Supervisor routed request to restaurants")
        return {**state,"next": "restaurants"}

    elif any(word in query for word in hotel_keywords):
        logger.info("Supervisor routed request to hotels")
        return {**state,"next": "hotels"}

    elif any(word in query for word in attraction_keywords):
        logger.info("Supervisor routed request to attractions")
        return {**state,"next": "attractions"}

    elif any(word in query for word in budget_keywords):
        logger.info("Supervisor routed request to budget")
        return {**state,"next": "budget"}

    else:
        logger.info("Supervisor routed request to RAG")
        return {**state,"next": "rag"}


# ---------------- PLANNER AGENT ----------------
def planner_agent(state):

    query = state["input"]
    logger.info("Planner agent started")

    prompt = f"""
    You are a world-class travel planner.
    
    Create a detailed travel Itinerary for: {query}
    
    Do not generate multiple itineraries.
    Requirements:
    - Organize each day into Morning, Afternoon, and Evening.
    - Include real attractions and restaurants.
    - Group nearby attractions together.
    - Avoid excessive travel between locations.
    - Include a brief reason for each recommendation.
    - Use realistic timings.
    - Return clean JSON only.

    Rules:
   - If the destination is a continent (e.g. Europe, Asia),
     choose ONE realistic destination and create ONE itinerary only.
   - Return ONLY valid JSON.
   - Create exactly the number of days requested by the user.
   - If preferences are not provided, make reasonable assumptions.
   - Each day must contain:
     Morning, Afternoon, Evening
     - Each section must contain:
        Activity
        Location
        Details
        Time
    Do not return:
    - markdown`` ``
    - bullet points
    - explanations
    - multiple itineraries
    """

    response = llm.invoke(prompt)
    logger.info("Planner LLM call completed")
    content = response.content.strip()
    
    #json load error handling
    try:
        answer = json.loads(content)
        logger.info("Planner response parsed successfully")
    except Exception:
        logger.exception("Planner response failed JSON parsing")
        answer = {
        "error": "Failed to parse response",
        "raw_response": content
    }
    return {
        **state,
        "answer": answer,
        "source": "planner_agent"
    }


# ---------------- PLACES AGENT ----------------
def places_agent(state):
    logger.info("Places agent started")
    query = state["input"]

    logger.info("Calling places tool")
    result = places_mcp_tool(query)

    places = result.get("results",[])
    logger.info("Places tool returned %d results", len(places))

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
    You are a helpful travel assistant.

    The user asked: {query}

    Here are real places found nearby:
    {context}

    INSTRUCTIONS:
    - Present these results in a clear, friendly way.
    - Include the name, rating, and address for each place.
    - Do not invent additional places not listed above.
    - Do not create a multi-day itinerary.
    - - If there are no places listed above, ask the user to specify a city or location.
    """)
    logger.info("Places response generated")
    return {
        **state,
        "answer": response.content,
        "source": "🤖places_agent"
    }


# ---------------- RAG AGENT ----------------
def rag_agent(state):

    query = state["input"]
    logger.info("RAG agent started")

    logger.info("Running RAG retrieval")
    result = rag_mcp_tool(query)

    if isinstance(result, dict):
          context = result.get("results", "")
    else:
         context = str(result)
    
    response = llm.invoke(f"""
    You are a travel assistant.
                          
    Answer the user's question using ONLY this context.
    If the context does not contain the answer, say:
    "I don't have information about that in my knowledge base."
    Do not make up information that is not in the context.
    Context:
    {context}

    User query:
    {query}
    """)
    
    logger.info("RAG response generated")
    return {
        **state,
        "answer": response.content,
        "source": "🤖rag_agent"
    }