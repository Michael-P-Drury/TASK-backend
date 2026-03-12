from ..ai_capability.rag import perform_rag

async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = "searches teacher uploaded resources for helpful context, good to run when creating any class resources"

    return tool_description


async def run_tool(username, support_info):
    
    prompt = support_info['task']

    prompt = f'Search query: {prompt}' 

    relevant_chunks = await perform_rag(username, prompt, 5)

    response = '\n'.join(relevant_chunks)

    response = F'Relevant teacher support resources:\n{relevant_chunks}'

    return {'tool_id': 'search_teacher_resources', 'response': response}

