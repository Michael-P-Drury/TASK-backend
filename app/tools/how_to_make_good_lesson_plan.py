
async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'Guidance for how to make a lesson plan'

    return tool_description


async def run_tool(username, support_info):
    '''
    Runs tool
    '''
    
    response = '''
    To make a good lesson plan:
    
    - Must include a Hook.
    - A teacher must show passion for the subject (include intersting information to ensure teacher is passionate baout subject).
    - Must include contextual relevance to prevent 'domain knowledge'.
    - clear and simple objectives so teacher can go back and check on progress.
    - backup plan or time filling activities to handle unpredictable circumstances in a primary school lesson.
    '''
    
    return {'tool_id': 'how_to_make_good_lesson_plan', 'response': response}