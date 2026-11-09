from lession_001_prompting_generate_data_set import PromptEvaluator
from lesson_001_requests import add_user_message, chat

model = "claude-haiku-4-5"

def run_prompt(prompt_inputs):
    prompt = f"""
        Write a SQL extract query for Detail Design based on the Base Design Requirement. 
        
        - Overview: {prompt_inputs["Overview"]}
        - Table Schema: {prompt_inputs["Table Schema"]}
        - Mapping: {prompt_inputs["Mapping"]}
                
        **Guidelines**
        1. **Complete Column Selection:** Explicitly `SELECT` every single column and attribute specified in the Mapping documentation across all tables (e.g., IDs, dates, amounts, statuses, flags). Do not omit any mapped fields or rely solely on implicit filtering.
        2. **Precise Grouping & Aggregation:** When the business requirement or mapping specifies aggregations (e.g., grouped by customer, payment method, etc.), the `GROUP BY` clause must *only* include those specific grouping dimensions. Non-aggregated metric or attribute columns must use appropriate aggregate functions (e.g., `SUM`, `COUNT`, `MAX`, `MIN`) rather than blindly grouping by every selected column.
        3. **Strict ORDER BY Compliance:** The `ORDER BY` clause must *strictly* reference columns that are explicitly present in the `SELECT` clause (or valid aggregate aliases). Never include unselected columns in `ORDER BY` to ensure full compatibility with strict SQL standards across database platforms (such as SQL Server, PostgreSQL, and MySQL with `ONLY_FULL_GROUP_BY`).
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
        - All of column in Mapping must be Selected.
        - The where, join Clauses are all correct
        - The Order by are all correct.
        - The security and the performance of the SQL
    """
)

print(results)