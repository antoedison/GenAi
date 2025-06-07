
from google import genai

client = genai.Client(api_key="AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90")

def get_completion (content):
    response = client.models.generate_content(
        model="gemini-2.0-flash", 
        config= genai.types.GenerateContentConfig(
            system_instruction = "You are an expert in writing professional emails .",
            temperature = 0.3,
            top_p = 0.1,
            max_output_tokens = 50,
            
            ),
            contents= content
    )
    return response

content = input()
response = get_completion(content)
print(response.text)
print(len(response.text.split()))

"""
from google import genai

# Configure the API key
client = genai.Client(api_key="AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90")

def get_response(content):
    # Create a GenerateContentConfig object
    response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction="You are an expert in writing emails. If there is no information about email, then behave like a friendly chatbot.",
                temperature=0.3,
                top_p=0.1,
                max_output_tokens=1024),
            contents=user_input
        )
    return response.text



print("🤖 Hello! I am your AI Email Assistant. Ask me to write any email or message for you.")
print("Type 'exit' anytime to leave the chat.\n")

while True:
    user_input = input("📝 Enter your prompt: ")

    if user_input.strip().lower() == "exit":
        print("👋 Goodbye! Have a great day.")
        break

    # Generate email response
    try:
        user_response = get_response(user_input)
        print("\n📧 Generated Email:\n")
        print(user_response)
    except Exception as e:
        print(f"⚠️ Error generating response: {e}")
        continue

    # Ask if changes are needed
    while True:
        edit = input("\n✏️ Do you want to make any changes? (yes/no): ").strip().lower()
        if edit == "yes":
            user_input = input("🔁 Please describe what changes you'd like: ")
            combined_prompt = f""Here is the original email:\n{user_response}\n\nPlease modify it based on the following request:\n{user_input}""
            try:
                user_response = get_response(user_input)
                print("\n📧 Updated Email:\n")
                print(user_response)
            except Exception as e:
                print(f"⚠️ Error generating updated response: {e}")
                break
        elif edit == "no":
            print("✅ Great! Let me know if you want help with another email.\n")
            break
        else:
            print("Please respond with 'yes' or 'no'.")
"""