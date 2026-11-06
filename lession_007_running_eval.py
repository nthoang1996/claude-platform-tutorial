import json
import re
import ast
from statistics import mean

from lesson_001_requests import add_user_message, chat, add_assistant_message

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def run_prompt(test_case):
    model = "claude-haiku-4-5"
    messages = []
    
    prompt = f"""
        Please solve the follwing task:
        {test_case["task"]}
        
        * Respond only with Python, JSON, or a plain Regex
        * Do not add any comments or commentary or explanation
    """
    
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```code")
    
    return chat(messages, model=model, stop_sequences=["```"])

def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    else:
        return validate_regex(response)

def grade_by_model (test_case, output):
    eval_prompt = f"""
        You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.
        
        Original Task:
        <task>
        {test_case["task"]}
        </task>
        
        Solution to Evaluate:
        <solution>
        {output}
        </solution>
        
        Output Format
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key strengths
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1-10
        
        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
    """
    model = "claude-haiku-4-5"
    messages = []
    
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    eval_text = chat(messages, stop_sequences=["```"], model=model)
    
    return json.loads(eval_text)

def run_test_case(test_case):
    output = run_prompt(test_case)
    
    model_grade = grade_by_model(test_case, output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]
    
    syntax_score = grade_syntax(output, test_case)
    score = (model_score + syntax_score) / 2
    
    return {
        "output": output,
        "test_Case": test_case,
        "score": score,
        "reasoning": reasoning
    }
    
def run_eval(dataset):
    results = []
    
    for test_case in dataset:
        results.append(run_test_case(test_case))
        
    average_score = mean([result["score"] for result in results])
    print(average_score)
        
    return results

with open("dataset.json", "r") as f:
    dataset = json.load(f)
    
results = run_eval(dataset)

print(json.dumps(results, indent=2))