from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import os

# Step 1: Set Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90"  # Replace with actual key

# Step 2: Create a ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template("Tell me a joke about {topic}")

# Step 3: Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# Step 4: Use LangChain's new RunnableSyntax (pipeline)
chain = prompt_template | llm

# Step 5: Invoke the chain
response = chain.invoke({"topic": "cats"})

# Step 6: Print the output
print("🤖 Gemini says:", response.content)
