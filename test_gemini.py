from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# for model in genai.list_models():
#     if 'generateContent' in model.supported_generation_methods:
#         print(model.name)

llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")
response = llm.invoke("say hello in one sentence.")
print(response.content)
