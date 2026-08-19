#UI and main app logic
from dotenv import load_dotenv
load_dotenv()
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = "travel-planner"

from database.mongo_db import (
        init_db,
        save_message,
        load_chat_history,
        clear_history
)
from utils.logger import logger
import streamlit as st
from chains.answer_chain import answer_chain
from chains.critique_chain import critique_chain
from core.agent import run_agent
import uuid
from graph.react_agent import react_agent_executor


#-----------------Initialize DB---------------
init_db()

#---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Travel Agent")


# ---------------- SESSION STATE ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---------------- UI ----------------
st.title("🌍 AI Travel Planner Agent")

with st.expander("How it works"):
    st.write("""
    Multi-Agent AI system using:
    - LangGraph
    - RAG
    - Google Places API
    - Agent routing
    """)

show_debug = st.checkbox("Show Debug Info")

agent_mode = st.radio("Agent Mode", ["Supervisor (Default)", "ReAct Agent (Experimental)"])
# ---------------- CHAT HISTORY ----------------
history = []

history = load_chat_history(st.session_state.session_id)

for doc in history:
    role = doc.get("role", "")
    message = doc.get("message", "")

# ---------------- USER INPUT ----------------
user_query = st.chat_input("Ask your travel question...")

# ---------------- MAIN LOGIC ----------------
if user_query:

    logger.info("Travel request received")
     # show user message
    with st.chat_message("user"):
        st.markdown(user_query)

    # Save user message
    save_message(st.session_state.session_id, 
                 "user", 
                 user_query)

    #Run multiple agents
    with st.spinner("Thinking..."):

       try:
           if agent_mode == "ReAct Agent (Experimental)":
              react_response = react_agent_executor.invoke({
                "messages": [{"role": "user", "content": user_query}]
            })
              answer = react_response["messages"][-1].content
              source = "react_agent"
              steps = []
           else:
              response = run_agent(user_query, 
                             st.session_state.session_id)
            
              answer = response.get("answer", "")
              source = response.get("source", "unknown")
              steps = response.get("steps", [])

           logger.info("Agent workflow completed successfully")

       except Exception:

        logger.exception("Travel agent workflow failed")

        st.error(
            "Something went wrong while processing your request."
        )

        st.stop()
        
    ##Critique the answer
    critique = critique_chain.invoke({
        "question": user_query,
        "answer": answer
    })
    #decision step(hallucination check)
    if "yes" in critique.lower():
         final_answer = answer_chain.invoke({"question": user_query})
    else:
         final_answer = answer
         
    #show assistant response
    with st.chat_message("assistant"):
         if isinstance(final_answer, dict):
              st.json(final_answer)
         else:
              st.markdown(final_answer)

         if show_debug:
                 st.caption(f"Agent Used: 🤖 {source}")
             
    # Save assistant response
    save_message(st.session_state.session_id, 
                 "assistant", 
                 final_answer)
    
#--------CLEAR CHAT HISTORY--------
st.divider()

if st.button("🗑️ Clear Chat"):

    clear_history(st.session_state.session_id)

    st.rerun()