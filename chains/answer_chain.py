#answer prompt chain
from config.config import llm,parser
from langchain_core.prompts import ChatPromptTemplate

answer_prompt= ChatPromptTemplate.from_template(
   """
     "You are a helpful travel assistant. " \
    "Answer the following question: {question}"
    """
)

answer_chain = answer_prompt | llm | parser

