from lession_001_prompting_generate_data_set import PromptEvaluator
from lesson_001_requests import add_user_message, chat

model = "claude-haiku-4-5"

def run_prompt(prompt_inputs):
    prompt = f"""
        Extract key topics mentioned from a passage of text from a scholarly journal into a JSON array of strings.
        
        <text>
        {prompt_inputs["content"]}
        </text>
        
        Follow these steps:
        1. Closely examine the provided text
        2. Identify each topic mentioned
        3. Add each topic to a JSON array
        4. Respond with the JSON array. Do not provide any other text or commentary.
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages, model=model)

evaluator = PromptEvaluator(max_concurrent_tasks=5)

results = evaluator.run_evaluation(
    run_prompt_function=run_prompt, 
    dataset_file="dataset_article.json",
    extra_criteria="""
        - Contains a JSON array of strings, containing each topic mentioned in the article.
        - The strings should contain only a topic without any extra commentary
        - Response should contain the JSON array and nothing else.
    """
)

print(results)