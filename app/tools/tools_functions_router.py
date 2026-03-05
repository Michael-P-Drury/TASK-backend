import importlib


async def get_run_tool_function(tool_id: str):
    '''
    inputs:
    tool_id : str - the tool id for the tool you want the get tool's run function for

    outputs:
    func : function - the function for running the run function for tool
    
    takes input of tool id and returns function for running tool
    '''

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'run_tool')

    return func


async def get_create_resource_tool_function(tool_id: str):
    '''
    inputs:
    tool_id : str - the tool id for the tool you want the get tool's run function for

    outputs:
    func : function - the function for running the create resouces function for tool
    
    takes input of tool id and returns function for creating resources
    '''

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'create_resource')

    return func


async def get_rerun_tool_function(tool_id: str):
    '''
    inputs:
    tool_id : str - the tool id for the tool you want the get tool's run function for

    outputs:
    func : function - the function for running the create resouces function for tool
    
    takes input of tool id and returns function for creating resources
    '''

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'rerun_tool')

    return func


async def get_tool_description_function(tool_id: str):
    '''
    inputs:
    tool_id : str - the tool id for the tool you want the get tool decription function for

    outputs:
    func : function - the function for getting description for tool
    
    takes input of tool id and returns function for getting description for tool
    '''

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'get_tool_description')

    return func


async def get_tool_requirements_function(tool_id: str):
    '''
    inputs:

    tool_id : str - the tool id for the tool you want the get tool requirements function for
    
    takes input of tool id and returns function for getting requirements for tool
    '''

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'get_tool_requirements')

    return func