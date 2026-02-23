
async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'check quality of lesson plans'

    return tool_description


async def run_tool():
    
    response = 'Hello :)'
    
    return {'tool_id': 'check_lesson_plan_quality', 'response': response}