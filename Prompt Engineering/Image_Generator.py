import os
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

from google import genai
from google.genai import types

# Load API key from .env
load_dotenv()
api_key = os.getenv("google_api_key")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

# Step 1: Get image path and load it
image_path = input("Enter image file path (e.g., 'my_folder/photo.jpg'): ")
image = Image.open(image_path)

# Step 2: Convert image to bytes (PNG format recommended)
buffer = BytesIO()
image.save(buffer, format="PNG")
image_bytes = buffer.getvalue()

# Step 3: Get editing instruction
edit_prompt = input("What would you like to do with the image? ")

# Step 4: Send image and prompt to Gemini
response = client.models.generate_content(
    model="gemini-1.5-pro",  # Ensure you're using a model that supports images
    contents=[
        types.Content(
            parts=[
                types.Part(
                    inline_data=types.Blob(
                        mime_type="image/png",
                        data=image_bytes
                    )
                ),
                types.Part(
                    text=edit_prompt
                )
            ]
        )
    ],
    config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
)

# Step 5: Handle the response
for part in response.candidates[0].content.parts:
    if part.text:
        print("Gemini Text Response:\n", part.text)
    elif part.inline_data:
        edited_image = Image.open(BytesIO(part.inline_data.data))
        edited_image.save("edited_output.png")
        edited_image.show()
