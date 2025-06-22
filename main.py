# main.py
import os # env interacting tools
from dotenv import load_dotenv # tool to read .env files
from google import genai # get google generative ai tools

# Get env vars
load_dotenv() # read the .env file
api_key = os.environ.get("GEMINI_API_KEY") # get apikey from .env

# Create Google Generative AI client
client = genai.Client(api_key=api_key)

# send gen AI request
model = "gemini-2.0-flash-001"
prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

GeminiResp = client.models.generate_content(
    model=model, # version of gemini
    contents=prompt, # our prompt to AI
)

# get response fields
GeminiText = GeminiResp.text
GeminiPromptTokens = GeminiResp.usage_metadata.prompt_token_count
GeminiResponseTokens = GeminiResp.usage_metadata.candidates_token_count

# print response with token usage
print(GeminiResp.text) # print the gen ai response
print(f"Prompt tokens: {GeminiPromptTokens}") # tokens in the prompt
print(f"Response tokens: {GeminiResponseTokens}") # tokens in the response