import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate # Import PromptTemplate

import os
from dotenv import load_dotenv

# Load environment variables from .env file at the very beginning
load_dotenv()

def initialize_chatbot():
    """
    Initializes the Langchain components for the chatbot using Google Generative AI,
    fetching the API key from environment variables, and incorporating a PromptTemplate.
    """
    try:
        google_api_key = os.getenv("google_api_key")

        if not google_api_key:
            st.error("Google API Key not found. Please set the GOOGLE_API_KEY "
                     "environment variable in your .env file.")
            return None

        # Define the PromptTemplate
        # This template will guide the model on how to respond.
        # We can add instructions to be concise, focus on a specific topic, etc.
        template = """
        You are a friendly and helpful AI assistant.
        Your goal is to provide answers that are not too big.
        It have to crisp and clear.
        If a response is naturally longer, try to summarize it without losing key information.
        You have to translate your answer in tamil and return to the user.
        
        Current conversation:
        {history}
        Human: {input}
        AI:
        """
        PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)


        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

        memory = ConversationBufferMemory()

        # Pass the PROMPT to the ConversationChain
        conversation = ConversationChain(llm=llm, memory=memory, prompt=PROMPT, verbose=True)
        return conversation
    except Exception as e:
        st.error(f"Error initializing chatbot: {e}. "
                 "Ensure your Google API Key is valid and set correctly in .env.")
        return None

def main():
    st.set_page_config(page_title="Gemini Memory Chatbot", layout="centered")

    st.title("🧠 Gemini Memory Chatbot")
    st.write("This chatbot remembers past conversations using Langchain's ConversationBufferMemory with Google Gemini. "
             "Your API key is loaded securely from an environment file.")

    if "chatbot_conversation" not in st.session_state:
        st.session_state.chatbot_conversation = initialize_chatbot()

    if st.session_state.get("chatbot_conversation") is None:
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Say something..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chatbot_conversation.predict(input=prompt)

                with st.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred while getting a response: {e}")
                st.session_state.messages.append({"role": "assistant", "content": "Oops! Something went wrong. Please try again."})

if __name__ == "__main__":
    main()