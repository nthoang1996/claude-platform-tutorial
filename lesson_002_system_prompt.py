from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_001_requests import add_user_message, chat

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"

messages = []
system = """
    You are a patient math tutor.
    Do not directly answer the student's questions.
    Guide them to a solution step by step
"""

add_user_message(messages, "How do I solve 5x+3=2 for x")
answer = chat(messages, system)

print(answer)
