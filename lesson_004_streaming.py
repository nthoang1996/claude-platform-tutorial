from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_001_requests import add_user_message, chat

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"

messages = []

add_user_message(messages, "Write a sentence description of a fake database")

params = {
    "model": model,
    "max_tokens": 1000,
    "messages": messages
}

with client.messages.stream(**params) as stream:
    for text in stream.text_stream:
        print(text, end="")
    
# stream.get_final_message()
