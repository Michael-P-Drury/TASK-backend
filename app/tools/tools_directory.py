from.tools_functions_router import get_tool_description_function


tools_dict = {
    'create_exercise_sheet': 'main',
    'create_lesson_plan': 'main',
    'how_to_make_good_lesson_plan': 'support',
    'how_to_make_good_exercise_sheet': 'support',
    'check_lesson_plan_quality': 'quality',
    'check_exercise_sheet_quality': 'quality'
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

