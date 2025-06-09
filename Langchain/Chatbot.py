import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv # Import to load environment variables

# Load environment variables from .env file at the very beginning
load_dotenv()

def initialize_chatbot():
    """
    Initializes the Langchain components for the chatbot using Google Generative AI,
    fetching the API key from environment variables.
    """
    try:
        # Retrieve the Google API key from environment variables
        # It's crucial that GOOGLE_API_KEY is set in your .env file
        google_api_key = os.getenv("google_api_key")

        if not google_api_key:
            st.error("Google API Key not found. Please set the GOOGLE_API_KEY "
                     "environment variable in your .env file.")
            return None

        # Use ChatGoogleGenerativeAI for chat models like Gemini
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

        # Initialize ConversationBufferMemory to store chat history
        memory = ConversationBufferMemory()

        # Create a ConversationChain that links the LLM and memory
        conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
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

    # Initialize the chatbot once using the key loaded from .env
    if "chatbot_conversation" not in st.session_state:
        st.session_state.chatbot_conversation = initialize_chatbot()

    # If chatbot initialization failed (e.g., API key missing or invalid), stop here
    if st.session_state.get("chatbot_conversation") is None:
        return

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input in the chat interface
    if prompt := st.chat_input("Say something..."):
        # Display user message in the chat container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            try:
                # Get chatbot response from the Langchain ConversationChain
                response = st.session_state.chatbot_conversation.predict(input=prompt)

                # Display assistant response in the chat container
                with st.chat_message("assistant"):
                    st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred while getting a response: {e}")
                st.session_state.messages.append({"role": "assistant", "content": "Oops! Something went wrong. Please try again."})

if __name__ == "__main__":
    main()
