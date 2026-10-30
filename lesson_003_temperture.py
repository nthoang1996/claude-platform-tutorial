from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_001_requests import add_user_message, chat

load_dotenv()

client = Anthropic()
# claude-sonnet-5-5 rejects `temperature`, so this lesson uses a model that accepts it
model = "claude-sonnet-4-5"

messages = []

add_user_message(messages, "Name a random animal")
answer = chat(messages, temperature=0.0, model=model)

print(answer)
