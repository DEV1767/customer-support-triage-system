import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv


LLM=ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)
