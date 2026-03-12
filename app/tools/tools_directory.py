from .tools_functions_router import get_tool_description_function


tools_dict = {
    'create_exercise_sheet': 'main',
    'create_lesson_plan': 'main',
    'general_conversation': 'main',
    'how_to_make_good_lesson_plan': 'support',
    'how_to_make_good_exercise_sheet': 'support',
    'search_teacher_resources': 'support',
    'get_previous_output_for_changes': 'support',
    'get_previous_output_for_reference': 'support',
    'get_class_context': 'support',
    'check_lesson_plan_quality': 'quality',
    'check_exercise_sheet_quality': 'quality',
    'check_general_conversation_quality': 'quality'
}


main_tool_create_resouce_dict= {
    'create_exercise_sheet': True,
    'create_lesson_plan': True,
    'general_conversation': False,
}


linked_outputs = {
    'exercise_sheet.docx': ['teacher_version_exercise_sheet.docx'],
    'teacher_version_exercise_sheet.docx': ['exercise_sheet.docx']
}


async def get_tools_descriptions_text():

    tools = []

    for tool_id in tools_dict:

        func = await get_tool_description_function(tool_id)

        tool_description = await func()

        tool_class = tools_dict[tool_id]

        tools.append(f'{tool_id} |{tool_class} | {tool_description}')

    tools_descriptions_text = '\n'.join(tools)

    return tools_descriptions_text


async def create_support_tools_responses_text(support_tools_responses):
    '''
    inputs:
    support_tools_responses: list[dict] - list of dictionary items for each support tool response
    '''

    response_output = []

    for response_dict in support_tools_responses:
        tool_id = response_dict['tool_id']
        tool_response = response_dict['response']

        response_output.append(f'{tool_id}:\n{tool_response}')

    if response_output:

        return '\n'.join(response_output)
    
    return ''