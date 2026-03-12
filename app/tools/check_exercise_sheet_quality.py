from ..ai_capability.genai_call import invoke_genai


async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'check quality of worksheets'

    return tool_description


async def run_tool(task_information: str, main_tool_response: str, support_tool_responses: str):
    
    prompt = f'''

    You are a primary school exercise sheet quality check tool, your one job is to determine if an exercise sheet created is acceptable quality:

    Here is an exercise sheet created by GenAI:

    {main_tool_response}

    Here was the chat context that it created the resource from:

    {task_information}

    The genai was given this support information to help it create its resource:

    {support_tool_responses}

    Your one task is to proof read the exercise sheet created and check if there is anything wrong or that you think NEEDS to be improved:

    If you think that it is of acceptable quality, you must respond with:
    FALSE|Improvements for needed improvements

    If you think that the The quality of the exercise sheet is acceptable you must reply with:
    TRUE
    '''

    response_dict = await invoke_genai(prompt, 'cerebras', 'gpt-oss-120b', 0.7)

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
