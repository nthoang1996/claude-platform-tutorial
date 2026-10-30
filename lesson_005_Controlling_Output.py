import json
from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_001_requests import add_assistant_message, add_user_message, chat

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"], model=model)

print(json.loads(text.strip()))