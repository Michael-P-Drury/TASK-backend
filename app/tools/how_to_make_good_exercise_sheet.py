
async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = 'guidance for exercisesheets/ worksheets'

    return tool_description


async def run_tool(username, support_info):
    '''
    output:
    str - tool response

    Runs tool
    '''
    
    response = '''
    Good exercise sheets must include:

    Scaffolding Strategies: Retrieve methods for "fading" support, such as including worked examples for the first three questions and then removing them.

    Differentiation Logic: Instead of "Easy/Medium/Hard" tiers, it should suggest "Adaptive Support" where the core content remains high-standard for all pupils but the hints vary.

    Curriculum Alignment: It should fetch specific "Action Verbs" from your teaching standards (e.g., "identify," "analyze," "evaluate") to ensure the worksheet hits the right level of Bloom's Taxonomy.
    '''
    
    return {'tool_id': 'how_to_make_good_exercise_sheet', 'response': response}