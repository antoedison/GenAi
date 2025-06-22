import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_chatbot():
    try:
        google_api_key = os.getenv("GOOGLE_API_KEY")

        if not google_api_key:
            st.error("Google API Key not found. Please set the GOOGLE_API_KEY in your .env file.")
            return None

        template = """
        You are a friendly and helpful AI assistant.
        Your goal is to provide answers that are not too long.
        They must be crisp and clear.
        If a response is naturally longer, try to summarize it without losing key information.
        If the user is feeling a little low(sad) console them and say some good words.
        The user must feel you as their best friend and heal their problems.
        Translate your final answer into the selected language: {language}

        Conversation history:
        {history}
        Human: {input}
        AI:"""

        prompt = PromptTemplate(
            input_variables=["history", "input", "language"],
            template=template
        )

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=google_api_key
        )

        memory = ConversationBufferMemory(memory_key="history", input_key="input", return_messages=False)

        conversation = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            verbose=True
        )
        return conversation

    except Exception as e:
        st.error(f"Error initializing chatbot: {e}")
        return None

def main():
    st.set_page_config(page_title="Friendly Chatbot", layout="centered",page_icon="..\Images\Project_logo.png")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Your Secret Friend 😜")
    with col2:
        language = st.selectbox("Select a language:", [
            "English", "Tamil", "Telugu", "Malayalam", "Kannada", "Hindi", "French", "Spanish"
        ])

    st.write(
        "A friend hidden in the silence of your screen 🤫 — I hear you, I understand you, and I’m here to help when no one else does.\n"
        "Talk to me in whatever language you're comfortable with."
    )

    if "chatbot_conversation" not in st.session_state:
        st.session_state.chatbot_conversation = initialize_chatbot()

    if st.session_state.chatbot_conversation is None:
        return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all chat history with avatars
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar", None)):
            st.markdown(message["content"])

    if prompt := st.chat_input("Say something..."):
        # Show user message and store it with avatar
        st.chat_message("user", avatar="🙂").markdown(prompt)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "avatar": "🙂"
        })

        with st.spinner("Thinking..."):
            try:
                response = st.session_state.chatbot_conversation.predict(
                    input=prompt,
                    language=language
                )
                # Show bot response and store it with avatar
                st.chat_message("assistant", avatar="Images/Chatbot_logo.png").markdown(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "avatar": "Images/Chatbot_logo.png"
                })
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Oops! Something went wrong. Please try again.",
                    "avatar": "Images/Chatbot_logo.png"
                })

if __name__ == "__main__":
    main()
