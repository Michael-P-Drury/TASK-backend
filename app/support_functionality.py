from .tools.tools_directory import tools_dict
from .user.user_account import get_user_chat_history, set_chat_history

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