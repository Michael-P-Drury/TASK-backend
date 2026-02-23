from .tools.tools_directory import tools_dict
from .user.user_account import get_user_chat_history, set_chat_history
import time
from .tools.tools_functions_router import get_run_tool_function
import asyncio
import pypandoc
import tempfile
import os

async def seperate_tools(decision_text):
    
    main_tool = ''
    support_tools = []
    quality_tools = []
    halucinated_tools = []
    extra_main_tools = []
    seperated_tools_text_list = []
    
    for tool in decision_text.split('\n'):
        tool_id = tool.strip()

        if tool_id in tools_dict.keys():

            tool_type = tools_dict[tool_id]

            if tool_type == 'main':
                if not main_tool:
                    main_tool = tool_id
                else:
                    extra_main_tools.append(tool_id)

            elif tool_type == 'support':
                support_tools.append(tool_id)
            
            else:
                quality_tools.append(tool_id)

        else:
            halucinated_tools.append(tool_id)

    if main_tool:
        seperated_tools_text_list.append(f'Main tool: *{main_tool}*')

    if support_tools:
        seperated_tools_text_list.append(f'Support tools: *{", ".join(support_tools)}*')

    if quality_tools:
        seperated_tools_text_list.append(f'Quality tools: *{", ".join(quality_tools)}*')

    if halucinated_tools:
        seperated_tools_text_list.append(f'Halucinated tools: *{", ".join(halucinated_tools)}*')

    if extra_main_tools:
        seperated_tools_text_list.append(f'Extra main tools: *{", ".join(extra_main_tools)}*')

    seperated_tools_text = '\n'.join(seperated_tools_text_list)

    return {'main_tool': main_tool, 'support_tools': support_tools, 'quality_tools': quality_tools, 'halucinated_tools': halucinated_tools, 'extra_main_tools': extra_main_tools, 'seperated_tools_text': seperated_tools_text}




async def add_chat_history(username, chat_sender, chat_message, full_history):

    current_chat_history = await get_user_chat_history(username, full_history)

    current_chat_history = current_chat_history['chat_history']

    if current_chat_history:
        new_chat_history = current_chat_history + '\n\n**' + chat_sender + ':**\n' + chat_message

    else:
        new_chat_history = '**' + chat_sender + ':**\n' + chat_message

    await set_chat_history(username, new_chat_history, full_history)

    return new_chat_history



async def run_support_tools(username, support_tools_list):
    async_tasks = []

    for tool in support_tools_list:

        support_func = await get_run_tool_function(tool)

        support_info = {}

        async_tasks.append(support_func(username, support_info))

    full_chat_history_text = f'Running support tools: {" ,".join(support_tools_list)}'

    support_tools_start = time.time()

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    support_tools_responses = await asyncio.gather(*async_tasks)

    support_tools_end = time.time()

    support_tools_time = support_tools_end - support_tools_start

    full_chat_history_text = f'Ran support tools: {" ,".join(support_tools_list)} in {support_tools_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return support_tools_responses



async def run_main_tool(username, main_tool, support_tools_responses, relevant_chat_context):
    full_chat_history_text = f'Running main tool: {main_tool}'

    main_tool_start = time.time()

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    main_func = await get_run_tool_function(main_tool)

    main_tool_response = await main_func(username, relevant_chat_context, support_tools_responses)

    main_tool_end = time.time()

    main_tool_time = main_tool_end - main_tool_start

    full_chat_history_text = f'Ran main tool: {main_tool} in {main_tool_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return main_tool_response



async def create_docx_from_markdown(markdown_text):
    '''
    inputs:
    markdown_text: str - string of markidown text that you want to turn in to word file contents

    output:
    bytes object

    use:
    converts input of markdown text into a word file bytes object.
    '''

    temp_out_file =  tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    
    temp_output_path = temp_out_file.name

    temp_out_file.close()
    
    pypandoc.convert_text(markdown_text, 'docx', format='md', outputfile=temp_output_path)
    
    with open(temp_output_path, 'rb') as f:
        docx_bytes = f.read()

    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

    return docx_bytes