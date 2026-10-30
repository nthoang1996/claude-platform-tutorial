from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)
    
def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)
    
def chat(messsages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messsages
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    
    return "".join(b.text for b in message.content if b.type == "text")

# messages = []

# add_user_message(messages, "Define quantum computing in one sentence")
# print(messages)

# answer = chat(messages)
# print(answer)

# add_assistant_message(messages, answer)
# print(messages)

# add_user_message(messages, "Write another sentence")
# print(messages)

# answer = chat(messages)
# print(answer)