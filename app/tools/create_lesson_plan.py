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


async def run_tool(username, task_information, support_tool_responses_text):
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


    response_dict = await invoke_genai(prompt, 'cerebras', 'qwen-3-235b-a22b-instruct-2507', 0.7)

    genai_response = response_dict['response']

    full_docx = await create_docx_from_markdown(genai_response)

    await upload_user_output_file(username, 'lesson_plan.docx', full_docx)     

    return {'tool_id': 'create_exercise_sheet', 'response': genai_response}


