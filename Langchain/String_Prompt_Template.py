import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI  # ✅ Correct import
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")
# ✅ Set your Google Gemini API key
#os.environ["GOOGLE_API_KEY"] = os.environ(api_key)

# ✅ Initialize the Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature = 0.6,
    google_api_key= api_key,
    verbose= True
    )

# ✅ Send a prompt to the model
#response = model.invoke("Explain the purpose of LangChain in simple terms.")

prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
filled_prompt = prompt_template.invoke({"topic": "cats"})

response = model.invoke(filled_prompt)
# ✅ Print the model's response
print(response.content)






