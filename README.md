# 🌍 TravelAI — Multi-Agent AI Travel Planning System

TravelAI is an advanced **multi-agent AI travel assistant** that generates intelligent, personalized travel itineraries using **LLMs, RAG (Retrieval-Augmented Generation), MCP tools, and graph-based workflow orchestration**.

It combines structured reasoning, external APIs, and dual-database memory systems to deliver accurate, context-aware travel planning.

---

# 🚀 Features

### 🧠 Multi-Agent Architecture
- Planner Agent (itinerary generation)
- QA Agent (general travel questions)
- Retrieval Agent (RAG-based knowledge search)
- Tool Agent (Places API / external tools)

---

### 📚 RAG-Based Knowledge System
- Uses `.txt` travel data for context-aware responses
- Embedding-based retrieval for relevant travel information
- Improves factual accuracy of itineraries

---

### 🧩 Graph-Based Workflow Engine
- Controlled execution flow using `graph.py`
- Ensures structured decision-making across agents
- Supports scalable multi-step reasoning pipelines

---

### 🔧 MCP Tool Integration
- Places API integration for real-world data
- Extensible tool system (`mcp_tools.py`)
- Supports hotels, restaurants, attractions, and maps

---

### 🗄️ Dual Database System
- **MongoDB** → Chat history + analytics + session memory
- **SQLite** → Structured travel data (users, itineraries, preferences)

Clear separation ensures scalability and reliability.

---

### 🧪 Response Quality Control
- Critique Chain evaluates generated itineraries
- Improves accuracy and reduces hallucinations
- Enhances structured output quality

---

### 🎨 Streamlit UI
- Interactive chat interface (`app.py`)
- Real-time itinerary generation
- Conversation history tracking

---

# 🏗️ System Architecture

User  
↓  
Streamlit UI (app.py)  
↓  
Agent Router (agent.py)  
↓  
Graph Workflow (graph.py)  
↓  
RAG System + MCP Tools + Multi-Agents  
↓  
Answer Chain → Critique Chain  
↓  
Final Response  
↓  
MongoDB (chat memory) + SQLite (structured data)

---

# 🧱 Project Structure

TravelAI/
│
├── app.py
├── dashboard.py
├──core 
   |---agent.py
   ├── agents.py
   ├── graph.py
   ├── state.py
   ├── models.py
│
├── chains/
│   ├── answer_chain.py
│   └── critique_chain.py
│
├── rag/
│   └── rag.py
│
├── tools/
│   └── mcp_tools.py
│
├── database/
│   ├── mongo_db.py
│   └── sqlite_db.py
│
├── data/
│   └── travel_data.txt
│
├── utils/
│
└── requirements.txt

---

# ⚙️ Tech Stack

- Python 🐍
- Streamlit 🎨
- Multi-Agent Systems 🤖
- RAG (Vector Search) 📚
- MongoDB 🍃
- SQLite 🗄️
- Places API 🌍
- LLMs (OpenAI / Mistral / GPT)

---

# 🔄 Data Flow

User Query  
↓  
Agent Router  
↓  
Graph Workflow Engine  
↓  
RAG Retrieval + MCP Tools  
↓  
Answer Chain Generation  
↓  
Critique Chain Validation  
↓  
Final Response  
↓  
MongoDB (chat + analytics)  
SQLite (structured travel data)

---

# 🧠 Key Design Decisions

✔ Separation of concerns  
- Chat memory → MongoDB  
- Structured data → SQLite  
- Reasoning → Agents + Chains  
- Execution → Graph workflow  

✔ Scalable multi-agent system  
✔ Tool-first architecture (MCP design)  
✔ Modular and production-ready structure  

---

# 📦 Installation

git clone https://github.com/your-username/TravelAI.git  
cd TravelAI  
pip install -r requirements.txt  

---

# ▶️ Run the App

streamlit run app.py  

---

# 🔑 Environment Variables

Create a `.env` file:

MONGO_URI=your_mongodb_connection_string  
OPENAI_API_KEY=your_api_key  

---

# 📊 Future Improvements

- LangGraph full migration  
- Flight + hotel booking APIs  
- Real-time pricing integration  
- Map-based itinerary visualization  
- Voice-based travel assistant  
- Personal travel memory system  

---

# 🧑‍💻 Author

Niharika Bisoyi  
AI Engineer | Multi-Agent Systems | RAG | LLM Applications  

---
