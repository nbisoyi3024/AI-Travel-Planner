#self critique chain
from config.config import llm, parser
from langchain_core.prompts import ChatPromptTemplate

critique_prompt = ChatPromptTemplate.from_template(
    """
    You are a strict travel AI reviewer.

    Review the following answer for:
    - correctness
    - clarity
    - completeness
    - hallucinations

    Answer:
    {answer}

    
    Return:
    1. Hallucination check (Yes/No)
    2. What is incorrect (if any)
    3. What should be fixed
    """
)

critique_chain = critique_prompt | llm | parser

