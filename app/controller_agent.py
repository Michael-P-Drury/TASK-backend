'''
Holds the controller agent functionality including run_controller_agent which acts as an entry for the controller agent and the proces flow functionality
'''


from .tools.tools_directory import get_tools_descriptions_text
from .genai.genai_call import invoke_genai
from .support_functionality import seperate_tools, add_chat_history, run_support_tools, run_main_tool, run_quality_tool, rerun_main_tool, run_create_resources
from .tools.tools_functions_router import get_tool_requirements_function, get_tool_description_function
from .tools.tools_directory import create_support_tools_responses_text



async def run_controller_agent(username: str, user_prompt: str):
    '''
    inputs:
    username: str - username for user chatting
    user_prompts: str - users input prompt

    outputs:
    json - {status, message} returning seccuessful status 200 or unsuccessful status 400 as well as response message
    '''

    # initialise sucessful status and message
    status = 200
    message = 'ran successfully'

    # add users message to the chat history both for full and condensed chat history
    condensed_chat_history = await add_chat_history(username, 'User', user_prompt, False) 
    await add_chat_history(username, 'User', user_prompt, True)

    # runs tool decision, deciding what tools are too be ran
    tool_decision_response = await make_tool_decision(condensed_chat_history)

    decision_text = tool_decision_response['response']
    decision_time = tool_decision_response['time_taken']

    # runs seperate tools to seperate outputs into dinctionary for each type of tool as well as text output for decided tools
    seperated_tools = await seperate_tools(decision_text)

    seperated_tools_text = seperated_tools['seperated_tools_text']

    # adds tool decidion to full chat history
    task_response = f'Tool Decision:\n{seperated_tools_text}\n*Time taken: {decision_time}s*'
    await add_chat_history(username, 'TASK', task_response, True)

    enough_info_response = await enough_info_decision(seperated_tools['main_tool'], condensed_chat_history)

    enough_info = enough_info_response['decision_bool']
    enough_info_text = enough_info_response['response']
    enough_info_time = enough_info_response['time_taken']

    task_response_full = f'Enough Information Decision:\n{enough_info_text}\n*Time taken: {enough_info_time}s*'

    if '|' in enough_info_text:
        post_decision_text = enough_info_text.split('|', 1)[1]
    else:
        post_decision_text = enough_info_text
    
    await add_chat_history(username, 'TASK', task_response_full, True)

    if not enough_info:
        await add_chat_history(username, 'TASK', post_decision_text, False)
    
    else:
        # runs support tools asyncrenously and creates 
        support_tools_responses = await run_support_tools(username, seperated_tools['support_tools'])

        # creates one string of text for responses
        support_tool_responses_text = await create_support_tools_responses_text(support_tools_responses)

        # runs main tool and sends response 
        main_tool_response = await run_main_tool(username, seperated_tools['main_tool'], support_tool_responses_text, post_decision_text)

        # runs support tool to check whether needs to re-run
        quality_check_response = await run_quality_tool(username, seperated_tools['quality_tool'], post_decision_text, main_tool_response, support_tool_responses_text)

        rerun = quality_check_response['rerun_decision']

        while rerun:

            improvements = quality_check_response['improvements']

            # runs main tool and sends response 
            main_tool_response = await rerun_main_tool(username, seperated_tools['main_tool'], support_tool_responses_text, post_decision_text, main_tool_response, improvements)

            # runs support tool to check whether needs to re-run
            quality_check_response = await run_quality_tool(username, seperated_tools['quality_tool'], post_decision_text, main_tool_response, support_tool_responses_text)

            rerun = quality_check_response['rerun_decision']

        await run_create_resources(username, seperated_tools['main_tool'], main_tool_response['full_response'])

        main_tool_response_text = main_tool_response['response']

        await add_chat_history(username, 'TASK', main_tool_response_text, True)
        await add_chat_history(username, 'TASK', main_tool_response_text, False)

    return {'status': status, 'message': message}


async def enough_info_decision(main_tool_id: str, chat_history: str):
    '''
    inputs:
    main_tool_id: str - the main tools id to test for
    chat_history: str - the chat history to use for context to check for enough information

    Used to make decision on whether the agent has enough information yet to run the main tool.
    '''


    # getting requirement and description for main tool to put into prompt
    requirements_func = await get_tool_requirements_function(main_tool_id)

    description_func = await get_tool_description_function(main_tool_id)

    main_tool_requirements = await requirements_func()

    main_tool_description = await description_func()

    prompt = f'''
    ### SYSTEM ROLE
    You are a binary classifier. Your ONLY job is to check if the Chat History contains the specific DATA POINTS required.

    ### REQUIRED DATA POINTS
    {main_tool_requirements}

    ### EVALUATION LOGIC
    1. Look at the "REQUIRED DATA POINTS" list.
    2. Search the "CHAT HISTORY" for a specific value for EACH point.
    3. If a data point is missing, the result is MISSING.

    ### OUTPUT RULES
    - IF ANY POINT IS MISSING: Output ONLY "FALSE" followed by a | and then a brief question to the user.
    - IF ALL POINTS ARE FOUND: Output ONLY "TRUE" followed by a | and then context from the chat that would be helpful for performing this task: {main_tool_description}
    - STRICT: No preamble, no "I understand," no "Based on the text."
    - reply with jsust your final decision

    ### CHAT HISTORY TO EVALUATE
    ---
    {chat_history}
    ---

    ### FINAL DECISION
    '''

    # run genai prompt and get response and tim taken ffrom invoke_genai function
    tool_decision_response = await invoke_genai(prompt, 'cerebras', 'gpt-oss-120b', 0.05)

    text_response = tool_decision_response['response']
    time_taken = tool_decision_response['time_taken']

    test_response = "".join(c for c in text_response if c.isalpha())

    # creating a boolean response from genai response
    if test_response.lower().strip().startswith('true'):

        return {'response': text_response, 'time_taken': time_taken, 'decision_bool': True}

    return {'response': text_response, 'time_taken': time_taken, 'decision_bool': False}



async def make_tool_decision(chat_history: str):
    '''
    inputs:

    chat_history: str - the chat history so that tool decisions can be made based on request
    '''

    # gets description of all of the tools in a formatted string for genai to decide against.
    tools_descriptions_string = await get_tools_descriptions_text()
        
    prompt = f'''
    You are a tool-selection engine. Your goal is to identify the specific IDs required to fulfill the user's last request.

    ### TOOL DATA:
    {tools_descriptions_string}

    ### RULES:
    1. You MUST select exactly ONE 'main' tool. If none apply, output "NONE" and stop.
    2. You may select at most ONE 'quality' tool that matches the 'main' tool.
    3. You may select 'support' tools only if they directly relate to the 'main' tool and chat requirements.
    4. Output ONLY the IDs. No categories, no bullets, no intro text.

    ### EXAMPLE:
    User: "Help me design a worksheet about dogs."
    Output:
    create_exercise_sheet
    check_exercise_sheet_quality
    how_to_make_good_exercise_sheet
    get_class_context

    ### CURRENT TASK:
    Chat History:
    {chat_history}

    OUTPUT:
    '''

    # get entire genai response and return
    tool_decision_response = await invoke_genai(prompt, 'cerebras', 'gpt-oss-120b', 0.05)

    return tool_decision_response

    
