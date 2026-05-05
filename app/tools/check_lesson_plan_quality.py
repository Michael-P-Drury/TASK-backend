from ..ai_capability.genai_call import invoke_genai



async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'check quality of lesson plans'

    return tool_description


async def run_tool(task_information: str, main_tool_response: str, support_tool_responses: str):
    '''
    route for running tool
    '''
    
    prompt = f'''
    You are a primary school lesson plan quality check tool, your one job is to determine if a lesson plan created is acceptable quality and without hallucinations/ factual errors:

    Here is a lesson plan created by GenAI:

    {main_tool_response}

    Here was the chat context that it created the resource from:

    {task_information}

    The genai was given this support information to help it create its resource:

    {support_tool_responses}

    Ensure that the created lesson plan follows the following rules:

    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.
    - Do not wrap the entire response in a code block.

    Your one task is to proof read the lesson plan created and check if there is anything wrong or that you think NEEDS to be improved:

    If you think that it is of acceptable quality, you must respond with:
    FALSE|Improvements for needed improvements

    If you think that the The quality of the lesson plan is acceptable you must reply with:
    TRUE|none
    '''

    response_dict = await invoke_genai(prompt, 'openrouter', 'qwen/qwen3-235b-a22b-2507', 0.7)

    response = response_dict['response']

    rerun_decision = True

    improvements = None

    if response.lower().strip().startswith('true'):
        rerun_decision = False

    else:
        if '|' in response:
            improvements = response.split('|', 1)[1]

        else:
            improvements = response.replace('FALSE', '', 1)
    
    return {'tool_id': 'check_exercise_sheet_quality', 'improvements': improvements, 'rerun_decision': rerun_decision}
