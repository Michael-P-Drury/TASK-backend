import importlib


async def get_run_tool_function(tool_id):
    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'run_tool')

    return func

async def get_tool_description_function(tool_id):

    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'get_tool_description')

    return func

async def get_tool_requirements_tool_function(tool_id):
    module_path =  f".{tool_id}"

    module = importlib.import_module(module_path, package = __package__)
    func = getattr(module, 'get_tool_requirements')

    return func