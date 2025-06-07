from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")

model = ChatGoogleGenerativeAI(
    model= "gemini-2.0-flash",
    google_api_key=api_key,
    temperature = 0.6,
    verbose= True
)

prompt_template = ChatPromptTemplate([
    ("system", "You are a roasting assistant"),
    ("user", "Tell me a joke about {topic}")
])

filled_template = prompt_template.invoke({'topic':'cat'})

response = model.invoke(filled_template)
print(response.content)