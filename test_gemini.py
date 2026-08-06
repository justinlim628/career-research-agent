import google.generativeai as genai
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()
genai.confi

# llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
# response = llm.invoke('say hello in one sentence.')
# print(response.content)