import streamlit as st
import requests
from langchain_core.tools import Tool
from config.config import GOOGLE_API_KEY
from dotenv import load_dotenv
load_dotenv()
import os


def get_places(query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    
    params = {
        "query": query,
        "key":os.getenv("GOOGLE_API_KEY")
    }

    response = requests.get(url, params=params,timeout=5)
    data = response.json()

    results = []

    for place in data.get("results", [])[:5]:
        results.append(
            f"{place['name']} | ⭐ {place.get('rating', 'N/A')} | {place.get('formatted_address', 'No address')}"
        )

    return results

#helper function that avoids calling the Places API repeatedly for the same query
@st.cache_data
def cached_places(query):
    return get_places(query)



def get_tools(retriever):
    from rag.rag import rag_search
    return [
        Tool(
            name="Travel Knowledge Base",
            func=lambda q: rag_search(retriever, q),
            description="Use for travel guides and general information"
        ),
        Tool(
            name="Place Search",
            func=cached_places,
            description="Use for real-time places like restaurants, hotels"
        )
    ]