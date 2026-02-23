from ..user.user_account import get_class_context_and_year

async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = "gets context specific to teacher's class, usefull for creating any class resources"

    return tool_description


async def run_tool(username, support_info):
    
    full_class_context = await get_class_context_and_year(username)

    user_data = full_class_context['user_data']

    year_group = user_data['year_group']

    class_context = user_data['class_context']

    response_list = []

    if year_group:
        response_list.append(f'Class year group: UK Year {year_group}')

    if class_context:
        response_list.append(f'Class context: {class_context}')

    if response_list:
        response = '\n'.join(response_list)

    else:
        response = 'No given class context'
    
    return {'tool_id': 'check_lesson_plan_quality', 'response': response}