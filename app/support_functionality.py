'''
support functionality for modularity in application for controller agent
'''

from .tools.tools_directory import tools_dict
from .user.user_account import get_user_chat_history, set_chat_history
import time
from .tools.tools_functions_router import get_run_tool_function, get_rerun_tool_function
import asyncio
import pypandoc
import tempfile
import os

async def seperate_tools(decision_text: str):
    '''
    inputs:

    decision_text: str - formats text response from genai of tyool decision into organised dictionary

    outputs:
    
    dict - seperated out dictionary for different types of tools for processing.


    seperates out genai text into organised dictionary for processing
    '''
    
    # initiates out different types of tools as empty strings/ lists
    main_tool = ''
    support_tools = []
    quality_tools = []
    halucinated_tools = []
    extra_main_tools = []
    seperated_tools_text_list = []
    
    # loops through each line in response (each tool decision is split by a new line) and gets tool type/ lack of presence from tools dictionary
    # adding it to string/ list for that tool
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

    # created out a formatted text list to be turned intop a string (to display to users adds readability).
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




async def add_chat_history(username: str, chat_sender: str, chat_message: str, full_history: bool):
    '''
    inputs:
    username: str - users username
    chat_sender: str - user or TASK (sender of the message to be added to chat)
    chat_message: str - the message to be saved
    full_history: bool - True if it is to be added to the full history and False if it is to be added to the condensed history

    outputs:
    chat_history: str - returns chat history to be used

    adds to chat history (condensed and full based on full_history bool)
    '''

    # gets the current history which is to be added to
    current_chat_history = await get_user_chat_history(username, full_history)
    current_chat_history = current_chat_history['chat_history']

    # there there is already a history, add to it and if not, initiate chat history, formatted in markdown
    if current_chat_history:
        new_chat_history = current_chat_history + '\n\n**' + chat_sender + ':**\n' + chat_message

    else:
        new_chat_history = '**' + chat_sender + ':**\n' + chat_message

    # sets the chat history
    await set_chat_history(username, new_chat_history, full_history)

    # returns the chat history
    return new_chat_history



async def run_support_tools(username: str, support_tools_list: list):
    '''
    inputs:
    username: str - users username
    support_tools_list: list[str] list of support tool ids to run

    outputs:
    list[str] - responses from all support tools

    runs support tools
    '''

    # initiaqlises async tasks to run
    async_tasks = []

    # loops through each support tool adding run function to async tasks to run
    for tool in support_tools_list:

        support_func = await get_run_tool_function(tool)

        support_info = {}

        async_tasks.append(support_func(username, support_info))

    # adds to full chat history that suport tools are running
    full_chat_history_text = f'Running support tools: {" ,".join(support_tools_list)}'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    # measures time to run and runs tasks

    support_tools_start = time.time()

    support_tools_responses = await asyncio.gather(*async_tasks)

    support_tools_end = time.time()

    support_tools_time = support_tools_end - support_tools_start

    # adds to full chat history that the support tools have ran

    full_chat_history_text = f'Ran support tools: {" ,".join(support_tools_list)} in {support_tools_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return support_tools_responses



async def run_main_tool(username: str, main_tool: str, support_tools_responses: list, relevant_chat_context: str):
    '''
    inputs:
    username: str - users username
    main_tool: str - id for main tool
    support_tool_responses: list[str] - list of responses from support tools
    relevant_chatr_context: str - relevant chat context for running main tool

    outputs:
    main_tool_response: str - response from main tool

    runs main tool adding to full chat history that it has ran with time to run
    '''

    # adds to full chat history that main tool is running
    full_chat_history_text = f'Running main tool: {main_tool}'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    # measure time to run and run main tool
    main_tool_start = time.time()

    main_func = await get_run_tool_function(main_tool)

    main_tool_response = await main_func(username, relevant_chat_context, support_tools_responses)

    main_tool_end = time.time()

    main_tool_time = main_tool_end - main_tool_start

    # add to full chat history that main tool has ran and with time to run then return response from main tool
    full_chat_history_text = f'Ran main tool: {main_tool} in {main_tool_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return main_tool_response


async def rerun_main_tool(username: str, main_tool: str, support_tools_responses: str, relevant_chat_context: str, previous_main_tool_response: str, improvements: str):
    '''
    inputs:
    username: str - users username
    main_tool: str - id for main tool
    support_tool_responses: list[str] - list of responses from support tools
    relevant_chatr_context: str - relevant chat context for running main tool
    previous_main_tool_response: str - previous response to improve
    improvements: str - recommedned improvements

    outputs:
    main_tool_response: str - response from main tool

    runs main tool adding to full chat history that it has ran with time to run
    '''

    # adds to full chat history that main tool is running
    full_chat_history_text = f'rerunning main tool: {main_tool}'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    # measure time to run and run main tool
    main_tool_start = time.time()

    rerun_func = await get_rerun_tool_function(main_tool)

    main_tool_response = await rerun_func(username, relevant_chat_context, support_tools_responses, previous_main_tool_response, improvements)

    main_tool_end = time.time()

    main_tool_time = main_tool_end - main_tool_start

    # add to full chat history that main tool has ran and with time to run then return response from main tool
    full_chat_history_text = f'rerunning main tool: {main_tool} in {main_tool_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return main_tool_response


async def run_create_resources(username: str, main_tool: str, crete_resource_information: str):
    '''
    inputs:
    username: str - users username
    main_tool: str - id for main tool
    support_tool_responses: list[str] - list of responses from support tools
    relevant_chatr_context: str - relevant chat context for running main tool

    outputs:
    main_tool_response: str - response from main tool

    runs main tool adding to full chat history that it has ran with time to run
    '''

    # adds to full chat history that main tool is running
    full_chat_history_text = f'Creating resource using main tool: {main_tool}'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    # measure time to run and run main tool
    main_tool_start = time.time()

    create_func = await get_run_tool_function(main_tool)

    main_tool_response = await create_func(username, crete_resource_information)

    main_tool_end = time.time()

    main_tool_time = main_tool_end - main_tool_start

    # add to full chat history that main tool has ran and with time to run then return response from main tool
    full_chat_history_text = f'Created resource using main tool: {main_tool} in {main_tool_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return main_tool_response
    



async def create_docx_from_markdown(markdown_text):
    '''
    inputs:
    markdown_text: str - string of markidown text that you want to turn in to word file contents

    output:
    bytes object

    converts input of markdown text into a word file bytes object.
    '''

    # creates a temporary file (needed to context to .docx)
    temp_out_file =  tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
    
    temp_output_path = temp_out_file.name

    temp_out_file.close()

    # use pypandoc to convert from markdown to docx file
    pypandoc.convert_text(markdown_text, 'docx', format='md', outputfile=temp_output_path)
    
    # reads file, removes file and returns docx file bytes
    with open(temp_output_path, 'rb') as f:
        docx_bytes = f.read()

    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

    return docx_bytes



async def run_quality_tool(username: str, quality_tool: str, post_decision_text: str, main_tool_response: str, support_tool_responses_text: str):
    '''
    inputs:
    username: str - users username
    quality_tool: str - id for quality tool
    support_tool_responses: list[str] - list of responses from support tools
    relevant_chatr_context: str - relevant chat context for running main tool

    outputs:
    quality_tool_response: str - response from quality tool

    runs quality tool adding to full chat history that it has ran with time to run
    '''

    # adds to full chat history that quality check tool is running
    full_chat_history_text = f'Running quality check tool: {quality_tool}'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    # measure time to run and run main tool
    quality_tool_start = time.time()

    quality_func = await get_run_tool_function(quality_tool)

    quality_tool_response = await quality_func(post_decision_text, main_tool_response, support_tool_responses_text)

    quality_tool_end = time.time()

    quality_tool_time = quality_tool_end - quality_tool_start

    # add to full chat history that quality check tool has ran and with time to run then return response from quality tool
    full_chat_history_text = f'Ran quality check tool: {quality_tool} in {quality_tool_time}s'

    await add_chat_history(username, 'TASK', full_chat_history_text, True)

    return quality_tool_response
