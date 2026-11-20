from anthropic import Anthropic
from anthropic.types import Message
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
model = "claude-sonnet-5-5"


def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(messages, Message) else messages,
    }
    messages.append(user_message)


def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(messages, Message) else messages,
    }
    messages.append(assistant_message)


def chat(
    messages,
    system=None,
    temperature=None,
    model=model,
    stop_sequences=None,
    tools=None,
):
    params = {"model": model, "max_tokens": 1000, "messages": messages}

    # SDK 1.0.0's create() has no temperature argument, so send it in the body
    if temperature is not None:
        params["extra_body"] = {"temperature": temperature}

    if tools:
        params["tools"] = tools

    if system:
        params["system"] = system

    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    return client.messages.create(**params)


def text_from_message(message):
    return "\n".join([block.text for block in message.content if block.type == "text"])


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
