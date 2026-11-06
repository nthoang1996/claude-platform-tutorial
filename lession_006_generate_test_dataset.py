import json

from lesson_001_requests import add_user_message, add_assistant_message, chat

model = "claude-haiku-4-5"


def generate_dataset():
    prompt = """
        Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
        that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
        each representing task that requires Python, JSON, or a Regex to complete.

        Example output:
        ```json
        [
            {
                "task": "Description of task",
                "format: "json" or "regex" or "python"
            },
            ...additional
        ]
        ```

        * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
        * Focus on tasks that do not require writing much code

        Please generate 3 objects.
    """
    
    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"], model = model)
    
    return json.loads(text)

dataset = generate_dataset()
print(dataset)

with open("dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)