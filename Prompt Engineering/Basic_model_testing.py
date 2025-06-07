from google import genai
# Configure the API key
client = genai.Client(api_key="AIzaSyAUU1Yh_VRUcGzsM6XDDy_a-_vsCIlcQ90")

# Create a model instance with system instructions
model = genai.Client(
    model="gemini-1.5-flash",
    system_instruction="You are an expert in writing emails. If there is no information about email, then behave like a friendly chatbot."
)

print("🤖 Hello! I am your AI Email Assistant. Ask me to write any email or message for you.")
print("Type 'exit' anytime to leave the chat.\n")

while True:
    user_input = input("📝 Enter your prompt: ")

    if user_input.strip().lower() == "exit":
        print("👋 Goodbye! Have a great day.")
        break

    # Generate email response
    try:
        response = client.models.generate_content(contents=user_input)
        print("\n📧 Generated Email:\n")
        print(response.text)
    except Exception as e:
        print(f"⚠️ Error generating response: {e}")
        continue

    # Ask if changes are needed
    while True:
        edit = input("\n✏️ Do you want to make any changes? (yes/no): ").strip().lower()
        if edit == "yes":
            user_input = input("🔁 Please describe what changes you'd like: ")
            try:
                response = model.generate_content(contents=user_input)
                print("\n📧 Updated Email:\n")
                print(response.text)
            except Exception as e:
                print(f"⚠️ Error generating updated response: {e}")
                break
        elif edit == "no":
            print("✅ Great! Let me know if you want help with another email.\n")
            break
        else:
            print("Please respond with 'yes' or 'no'.")
