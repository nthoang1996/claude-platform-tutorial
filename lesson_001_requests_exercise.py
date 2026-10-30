from dotenv import load_dotenv
from anthropic import Anthropic

from lesson_002_system_prompt import add_user_message, chat, add_assistant_message

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"

messages = []

while True:
    user_input = input("> ")
    add_user_message(messages, user_input)
    
    answer = chat(messages)
    
    add_assistant_message(messages, answer)
    
    print("---")
    print(answer)
    print("---")
