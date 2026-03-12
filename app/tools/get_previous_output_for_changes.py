from ..user.user_account import get_output_references


async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = "gets previously created output, specific for if user requests any changes to be made."

    return tool_description


async def run_tool(username: str, support_info):

    main_tool = support_info['main_tool']

    user_request = support_info['task']

    output_references = await get_output_references(username)

    content = ''

    for reference in output_references:
        if reference['tool_id'] == main_tool:
            content = ''

    response = f'previously created response:\n{content}\nUser has requested the following change:{user_request}'
    
    return {'tool_id': 'get_previous_output', 'response': response}