from ..genai.genai_call import invoke_genai
from ..data_storage.s3_functionality import upload_user_output_file
from ..support_functionality import create_docx_from_markdown


async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'creates exercise sheets / worksheets'

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
    Your task is to create a two-part educational resource based on this context:
    {task_information}

    OUTPUT STRUCTURE:
    You must provide exactly two sections, separated by the delimiter: ||

    Section 1: The Student Exercise Sheet
    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.

    ||

    Section 2: The Teacher Support Guide
    - 1 sentence saying that an exercise sheet file and teacher support file was created
    - Include a full Answer Key.
    - Provide reasoning for the decisions made.
    - Include any additional tips or context.
    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.

    RULES:
    - Formatted in clean Markdown.
    - Do not use LaTeX or math plugins; use standard text, bolding, and Unicode symbols for math.
    - Do not wrap the entire response in a code block.
    - Use the || delimiter exactly once.
    '''

    if support_tool_responses_text:
        prompt += f'\nHere is supporting information:\n{support_tool_responses_text}'

    response_dict = await invoke_genai(prompt, 'cerebras', 'qwen-3-235b-a22b-instruct-2507', 0.7)

    genai_response = response_dict['response']

    if '||' in genai_response:

        exercise_sheet = genai_response.split('||')[0]

        exercise_sheet_docx = await create_docx_from_markdown(exercise_sheet)

        await upload_user_output_file(username, 'exercise_sheet.docx', exercise_sheet_docx)

        teacher_support_file = genai_response.replace('||', '')

        teacher_support_docx = await create_docx_from_markdown(teacher_support_file)

        await upload_user_output_file(username, 'teacher_version_exercise_sheet.docx', teacher_support_docx)       
        
        return {'tool_id': 'create_exercise_sheet', 'response': teacher_support_file}
    
    else:

        full_docx = await create_docx_from_markdown(genai_response)

        await upload_user_output_file(username, 'teacher_version_exercise_sheet.docx', full_docx)     

        return {'tool_id': 'create_exercise_sheet', 'response': genai_response}


