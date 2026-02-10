import importlib


async def enough_info_decision(user_prompt, tool_id):
    '''
    Used to make decision on whether the agent has enough information yet to run tools.
    '''


    module_path =  f".tools.{tool_id}"

    module = importlib.import_module(module_path, package = __package__)

    func = getattr(module, 'get_tool_requirements')

    requirement = func(user_prompt)

    response = ''

    if response == '':
        return True

    else:
        return False



async def tool_decision(user_prompt):
    '''
    
    '''