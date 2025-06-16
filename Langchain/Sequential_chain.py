import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain, TransformChain
import json
import re

# Load environment variables (ensure GOOGLE_API_KEY is set in your .env file)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")

# Initialize the LLM (Gemini 1.5 Flash is a good choice for speed)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7, # A bit of creativity for language understanding
    google_api_key=GOOGLE_API_KEY,
    top_k=50,
    top_p=0.2,
    max_output_tokens=500, # Max tokens for LLM responses
)

# --- Chain 1: Language & Intent Analysis ---
# This chain identifies the text, source, and target languages.
analyze_intent_prompt = ChatPromptTemplate.from_template(
    """You are an expert linguistic assistant. Your task is to analyze the user's request
    and extract the following information:
    1. The core 'text' that needs to be translated.
    2. The 'source_language' of the given text. If not explicitly mentioned, try to infer it.
    3. The 'target_language' to which the text should be translated. If not explicitly mentioned, default to 'English'.

    Respond **ONLY** with a valid JSON object. Do not include any other text, explanations,
    or markdown fences (e.g., ```json). Ensure keys are "text_to_translate", "source_language", "target_language".

    Example format:
    {{
      "text_to_translate": "Hello",
      "source_language": "English",
      "target_language": "Spanish"
    }}

    User request: '{user_input}'
    """
)

analyze_intent_chain = LLMChain(
    llm=llm,
    prompt=analyze_intent_prompt,
    output_key="analysis_raw" # Output will be a JSON string
)

# --- Intermediate Step: Parse JSON from Chain 1's output ---
def parse_analysis_json(inputs: dict) -> dict:
    """Parses the 'analysis_raw' JSON string into individual keys."""
    raw_json_string = inputs["analysis_raw"]
    try:
        # Robustly find JSON within potential markdown blocks
        match = re.search(r"```(?:json)?\s*({.*})```", raw_json_string, re.DOTALL)
        if match:
            json_str_to_parse = match.group(1)
        else:
            json_str_to_parse = raw_json_string.strip()

        parsed_data = json.loads(json_str_to_parse)

        return {
            "text_to_translate": parsed_data.get("text_to_translate", ""),
            "source_language": parsed_data.get("source_language", "English"), # Default to English
            "target_language": parsed_data.get("target_language", "English") # Default to English
        }
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        print(f"Raw string failing to parse: '{raw_json_string}'")
        # Fallback to default values or original input in case of parsing failure
        return {
            "text_to_translate": inputs.get("user_input", ""),
            "source_language": "English",
            "target_language": "English"
        }
    except Exception as e:
        print(f"Unexpected error in JSON parsing: {e}")
        print(f"Raw string: '{raw_json_string}'")
        return {
            "text_to_translate": inputs.get("user_input", ""),
            "source_language": "English",
            "target_language": "English"
        }

parse_analysis_chain = TransformChain(
    input_variables=["analysis_raw", "user_input"], # user_input passed for fallback
    output_variables=["text_to_translate", "source_language", "target_language"],
    transform=parse_analysis_json
)

# --- Chain 2: Translation ---
# This chain performs the actual translation.
translate_prompt = ChatPromptTemplate.from_template(
    "Translate the following text from {source_language} to {target_language}. "
    "Respond **ONLY** with the translated text and nothing else. "
    "Text to translate: '{text_to_translate}'"
)

translate_chain = LLMChain(
    llm=llm,
    prompt=translate_prompt,
    output_key="translated_text"
)

# --- Chain 3: Content Examination & Reduction ---
# This chain checks the translated content and reduces it if deemed "unwanted" (e.g., too verbose).
# Define "unwanted content" in the prompt's instructions.
reduce_content_prompt = ChatPromptTemplate.from_template(
    """You are a content editor. Your task is to examine the provided translated text.
    If the text contains extraneous information, conversational filler, or is unnecessarily verbose
    for a direct translation, reduce it to its core meaning.
    If the translated text is already concise and direct, return it as is.
    Focus on retaining the essential information from the original text in the {target_language}.

    Original text (for context): '{text_to_translate}'
    Translated text to examine: '{translated_text}'

    Your refined translation (if reduced, or original if fine):
    """
)

reduce_content_chain = LLMChain(
    llm=llm,
    prompt=reduce_content_prompt,
    output_key="final_translated_text"
)

# --- Sequential Chain: Orchestrates the entire process ---
# Define the order of chains and how variables flow.
overall_translation_chain = SequentialChain(
    chains=[
        analyze_intent_chain,
        parse_analysis_chain,
        translate_chain,
        reduce_content_chain
    ],
    input_variables=["user_input"], # Only the initial input from the user
    output_variables=[
        "final_translated_text",
        "text_to_translate",
        "source_language",
        "target_language",
        "translated_text" # Keep the raw translation for comparison/debugging
    ],
    verbose=True # Set to True to see detailed chain execution
)

# --- Chatbot Interaction (Example Usage) ---
def chatbot_translate(user_query: str):
    print(f"\n--- Processing: '{user_query}' ---")
    try:
        response = overall_translation_chain.invoke({"user_input": user_query})
        print("\n*** Final Chatbot Response ***")
        print(f"Original Text: '{response.get('text_to_translate', 'N/A')}'")
        print(f"Source Language: '{response.get('source_language', 'N/A')}'")
        print(f"Target Language: '{response.get('target_language', 'N/A')}'")
        print(f"Raw Translated Text (before reduction): '{response.get('translated_text', 'N/A')}'")
        print(f"Final Translated Text: '{response.get('final_translated_text', 'N/A')}'")
        print("-" * 30)
        return response
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test cases
    chatbot_translate("Translate 'hello world' to French.")
    chatbot_translate("Can you put this into Spanish for me: How are you doing today?")
    chatbot_translate("नमस्ते, इसको अंग्रेजी में बताओ।") # Namaste, tell this in English (Hindi)
    chatbot_translate("Summarize and translate 'The quick brown fox jumps over the lazy dog repeatedly and with much enthusiasm.' to German.")
    chatbot_translate("What is the capital of France?") # Intent is not translation, will show how LLM handles it
    chatbot_translate("Please translate the following sentence to Italian: 'I am learning Italian and it is very interesting.' And make it concise.")