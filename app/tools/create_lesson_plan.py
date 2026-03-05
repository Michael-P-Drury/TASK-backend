from ..support_functionality import create_docx_from_markdown
from ..genai.genai_call import invoke_genai
from ..data_storage.s3_functionality import upload_user_output_file


async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'create lesson plans'

    return tool_description


async def get_tool_requirements():
    '''
    outputs:
    str - tool requirements

    Returns tool requirements
    '''

    tool_requirements = '1. Topic must be present in chat history: A specific topic for the exercise sheet.'

    return tool_requirements


async def run_tool(username: str, task_information: str, support_tool_responses_text: str):
    '''
    function to run tool

    inputs:
    support_tool_responses: str - text of support tool responses and names
    '''

    prompt = f'''
    Your task is to create an educational resource based on this context:
    {task_information}

    The resource must be a Lesson Plan.

    RULES:
    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.
    - Do not wrap the entire response in a code block.
    '''

    if support_tool_responses_text:
        prompt += f'\nHere is supporting information:\n{support_tool_responses_text}'

    response_dict = await invoke_genai(prompt, 'cerebras', 'gpt-oss-120b', 0.7)

    genai_response = response_dict['response']

    return {'tool_id': 'create_exercise_sheet', 'response': genai_response, 'create_resource_input': genai_response}


async def rerun_tool(username: str, task_information: str, support_tool_responses_text: str, previous_run_response, improvements):
    previous_prompt = f'''
    Your only task is to redo a task with given improvements

    Here was your previous task:

    Your task is to create an educational resource based on this context:
    {task_information}

    The resource must be a Lesson Plan.

    RULES:
    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.
    - Do not wrap the entire response in a code block.
    '''

    if support_tool_responses_text:
        previous_prompt += f'\nHere is supporting information:\n{support_tool_responses_text}'

    prompt = f'''
    Here was your previous task:

    {previous_prompt}

    You previously gave this output:

    {previous_run_response}

    Your task is not to create a new output with teh following improvements:

    {improvements}
    '''



async def create_resource(username: str, resource_input: str):
    '''
    inputs:
    username: str - users username
    resource_input: str - resource needed for input

    creates output lesson plan
    '''

    full_docx = await create_docx_from_markdown(resource_input)

    await upload_user_output_file(username, 'lesson_plan.docx', full_docx)
