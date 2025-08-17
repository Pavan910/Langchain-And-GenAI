""" from dotenv import load_dotenv
import os

load_dotenv()
print("Groq key:", os.getenv("GROQ_API_KEY")) """