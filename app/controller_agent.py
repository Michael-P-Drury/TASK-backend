from .tools.tools_directory import get_tools_descriptions_text
from .genai.genai_call import invoke_genai
from .support_functionality import seperate_tools, add_chat_history
from .tools.tools_functions_router import get_tool_requirements_tool_function


async def run_chat(username, user_prompt):

    status = 200
    message = 'ran successfully'

    condensed_chat_history = await add_chat_history(username, 'User', user_prompt, False) 
    await add_chat_history(username, 'User', user_prompt, True)

    tool_decision_response = await make_tool_decision(condensed_chat_history)

    decision_text = tool_decision_response['response']
    decision_time = tool_decision_response['time_taken']

    seperated_tools = await seperate_tools(decision_text)

    seperated_tools_text = seperated_tools['seperated_tools_text']

    task_response = f'Tool Decision:\n{seperated_tools_text}\n*Time taken: {decision_time}*'

    await add_chat_history(username, 'TASK', task_response, True)

    enough_info_response = await enough_info_decision(seperated_tools['main_tool'], condensed_chat_history)

    enough_info = enough_info_response['decision_bool']
    enough_info_text = enough_info_response['response']
    enough_info_time = enough_info_response['time_taken']

    task_response_full = f'Enough Information Decision:\n{enough_info_text}\n*Time taken: {enough_info_time}*'

    task_response_condensed = f'Enough Information Decision:\n{enough_info_text}'

    await add_chat_history(username, 'TASK', task_response_condensed, False)
    await add_chat_history(username, 'TASK', task_response_full, True)

    return {'status': status, 'message': message}



async def enough_info_decision(main_tool_id, chat_history):
    '''
    Used to make decision on whether the agent has enough information yet to run tools.
    '''

    func = await get_tool_requirements_tool_function(main_tool_id)

    main_tool_requirements = await func()

    prompt = f'''
    ### SYSTEM ROLE
    You are a binary classifier. Your ONLY job is to check if the Chat History contains the specific DATA POINTS required.

    ### REQUIRED DATA POINTS
    {main_tool_requirements}

    ### EVALUATION LOGIC
    1. Look at the "REQUIRED DATA POINTS" list.
    2. Search the "CHAT HISTORY" for a specific value for EACH point.
    3. If a data point is missing a specific subject or topic (e.g., the user asks for a "sheet" but doesn't say "Math"), the result is MISSING.

    ### OUTPUT RULES
    - IF ANY POINT IS MISSING: Output ONLY "FALSE" followed by a brief question to the user.
    - IF ALL POINTS ARE FOUND: Output ONLY "TRUE".
    - STRICT: No preamble, no "I understand," no "Based on the text."
    - reply with jsust your final decision

    ### EXAMPLES
    Example 1 (Missing Topic):
    History: "Make me an exercise sheet."
    Output: FALSE - What subject or topic should the exercise sheet cover?

    ### CHAT HISTORY TO EVALUATE
    ---
    {chat_history}
    ---

    ### FINAL DECISION
    '''

    print(prompt)

    tool_decision_response = await invoke_genai(prompt, 'ollama', 'llama3.1', 0.05)

    text_response = tool_decision_response['response']

    time_taken = tool_decision_response['time_taken']

    test_response = "".join(c for c in text_response if c.isalpha())

    if test_response.lower().strip().startswith('true'):

        return {'response': text_response, 'time_taken': time_taken, 'decision_bool': True}

    return {'response': text_response, 'time_taken': time_taken, 'decision_bool': False}



async def make_tool_decision(chat_history):

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

    ### CURRENT TASK:
    Chat History:
    {chat_history}

    OUTPUT:
    '''

    tool_decision_response = await invoke_genai(prompt, 'ollama', 'llama3.2:3b', 0.05)

    return tool_decision_response

    