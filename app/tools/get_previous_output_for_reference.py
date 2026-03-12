from ..user.user_account import get_output_references
from ..tools.tools_functions_router import get_tool_resource_function

async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = "gets previously created output, not for when changes are requested, for if previous response needed for reference."

    return tool_description


async def run_tool(username: str, support_info):
    '''
    inputs:
    username: str - users username
    support_info: dict - dict of support info
    '''

    output_references = await get_output_references(username)

    response = ''

    for reference in output_references:
        tool_id = reference['tool_id']

        func = await get_tool_resource_function(tool_id)

        resource = await func()

        content = reference['content']

        response += f'previously created {resource}:\n{content}\n'
    
    return {'tool_id': 'get_previous_output', 'response': response}
