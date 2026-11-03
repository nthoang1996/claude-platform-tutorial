import json
from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_001_requests import add_assistant_message, add_user_message, chat

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-5"

messages = []

add_user_message(messages, "Generate three different sample AWS CLI commands. Each should be very short")
add_assistant_message(messages, "Here are all three commands in al single block without any comments```:\nbash")

text = chat(messages, stop_sequences=["```"], model=model)

print(text)