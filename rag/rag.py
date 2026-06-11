#knowledge 
import os

from langchain_openai import OpenAIEmbeddings

from langchain_chroma import Chroma

DB_PATH = "chroma_db"

def load_rag():
     embeddings = OpenAIEmbeddings()

      # If DB already exists , just load it
     if os.path.exists(DB_PATH):
        db = Chroma(
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )
     else:
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
       
        loader = TextLoader("data/travel.txt")
        docs = loader.load()
     
        text_splitter = RecursiveCharacterTextSplitter(
           chunk_size=500,
           chunk_overlap=50
         )
        docs = text_splitter.split_documents(docs)

    

        db = Chroma.from_documents(documents=docs, 
                                embedding=embeddings,
                                persist_directory=DB_PATH)
     

     return db.as_retriever(search_kwargs={"k":5})


def query_rag(query):
    
    retriever = load_rag()
    
    docs = retriever.invoke(query)

    #remove duplicates
    unique_docs = list({doc.page_content: doc for doc in docs}.values())
    
    # convert to clean context string
    context = "\n\n".join([doc.page_content for doc in unique_docs])
    
    print("RAG CONTEXT:", context)
    
    return context

#-------RETRIEVER LOADING WITH CACHING-----
#@st.cache_resource
#def get_retriever():
 #   from rag import load_rag
  #  return load_rag()