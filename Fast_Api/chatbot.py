import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key="AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90")

# Use Gemini Flash
model = genai.GenerativeModel("gemini-2.0-flash")

def get_completion(content):
    prompt = f"""
You are a smart assistant that converts user queries into structured task objects.

Each response should be returned in **double-quoted JSON string** format like this:
"{{\"title\": \"some title\", \"description\": \"some description\", \"Completed\": false}}"

If the query is not understandable or unrelated to task management, reply with:
"Please provide a more specific or meaningful task."

User query: "{content}"
"""

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            top_p=0.1,
            max_output_tokens=100,
        )
    )
    return response.text.strip()

# Get user input
content = input("Enter your task query: ")
response = get_completion(content)

print("\nAssistant Response:")
print(response)
