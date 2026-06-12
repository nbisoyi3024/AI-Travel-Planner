#Logic for multiple agents: supervisor, planner, places, RAG
import json
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
    - markdown
    - bullet points
    - explanations
    - multiple itineraries
    """

    response = llm.invoke(prompt)
    
    content = response.content.strip()
    
    #json load error handling
    try:
        answer = json.loads(content)
    except Exception:
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
    
    You are an expert travel planner.

Create a travel itinerary for:
{query}

INSTRUCTIONS:

- Generate exactly ONE itinerary.
- If the user mentions a continent (e.g. Europe, Asia), choose ONE popular destination and build the itinerary around that destination only.
- Create exactly the number of days requested by the user.
- If the number of days is not specified, assume 3 days.
- If preferences are not provided, make reasonable assumptions.
- Use real attractions, restaurants, and landmarks.
- Group nearby attractions together.
- Minimize unnecessary travel.
- Use realistic timings.
- Include a short description for each activity.

OUTPUT FORMAT:

Return ONLY valid JSON.

Structure:

{{
  "Day 1": {{
    "Morning": {{
      "Activity": "",
      "Location": "",
      "Details": "",
      "Time": ""
    }},
    "Afternoon": {{
      "Activity": "",
      "Location": "",
      "Details": "",
      "Time": ""
    }},
    "Evening": {{
      "Activity": "",
      "Location": "",
      "Details": "",
      "Time": ""
    }}
  }}
}}

RULES:
- Do not return markdown.
- Do not use ```json.
- Do not add explanations before or after the JSON.
- Do not generate multiple itineraries.
- The response must start with {{ and end with }}.
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