from ..ai_capability.rag import perform_rag

async def get_tool_description():
    '''
    outputs:
    str - tool description

    Returns tool description
    '''
    
    tool_description = "searches resources for helpful context uploaded from the teacher, very important to run when creating any class resources or need to get context"

    return tool_description


async def run_tool(username, support_info):
    '''
    route for running tool
    '''
    
    prompt = support_info['task']

    prompt = f'Search query: {prompt}' 

    relevant_chunks = await perform_rag(username, prompt, 5)

    response = '\n'.join(relevant_chunks)

    response = F'Relevant teacher support resources:\n{relevant_chunks}'

    return {'tool_id': 'search_teacher_resources', 'response': response}

