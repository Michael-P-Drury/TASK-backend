
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

    Scaffolding Strategies: Effective exercise sheets incorporate scaffolding strategies, where initial tasks include structured support such as worked examples or prompts, which are gradually removed to promote independence.

    Differentiation Logic: Differentiation should be achieved through adaptive support rather than fixed tiers (e.g. easy/medium/hard), ensuring all pupils engage with the same high-quality content while varying the level of guidance provided.

    Curriculum Alignment: worksheets should align with curriculum expectations through the use of action verbs linked to Blooms Taxonomy, such as "identify", "explain", and "evaluate", ensuring appropriate cognitive challenge and progression.

    Challenge and Independence: Effective worksheets should include a final challenge task where scaffolding is fully removed, allowing pupils to apply their knowledge independently and demonstrating secure understanding.

    Assessment for Learning: Tasks should allow teachers to assess pupil understanding, for example through opportunities for explanation, reasoning, or application, rather than simple recall.
    '''
    
    return {'tool_id': 'how_to_make_good_exercise_sheet', 'response': response}