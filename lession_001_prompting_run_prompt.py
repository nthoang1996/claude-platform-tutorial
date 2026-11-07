from lession_001_prompting_generate_data_set import PromptEvaluator
from lesson_001_requests import add_user_message, chat

model = "claude-haiku-4-5"

def run_prompt(prompt_inputs):
    prompt = f"""
        Generate Detail Design for this Based Design below:
        
        - Sheet: {prompt_inputs["sheet"]}
        - Type: {prompt_inputs["type"]}
        - Mapping Sheet: {prompt_inputs["mapping_sheet"]}
        - Overview Sheet: {prompt_inputs["overview_sheet"]}
    """

    messages = []
    add_user_message(messages, prompt)
    return chat(messages, model=model)

evaluator = PromptEvaluator(max_concurrent_tasks=5)

results = evaluator.run_evaluation(
    run_prompt_function=run_prompt, 
    dataset_file="dataset_dd.json",
    extra_criteria="""
        The output should include:
        - The History of document
        - The flow chart and the description in the Overview sheet
        - The code python to transform data which can be referenced from the Overview sheet.
        Note that the transform will be processed by the Python Code.
        Do not use SQL to do this. The SQL just use to extract data from table.
        - The SQL Statement in the SQL Detail sheet which can be referenced from the Overview sheet.
        - If the sender is File. The SQL Detail sheet will be left empty.
    """
)

print(results)