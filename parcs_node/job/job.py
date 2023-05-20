import asyncio
import importlib
from collections import namedtuple

File = namedtuple('File', ['file_name', 'file_path'])


class Job:
    def __init__(self, solution_file: File):
        self.__solution_file = solution_file

    async def execute(self, *args, **kwargs):
        try:
            module = importlib.import_module(self.__solution_file.file_name)
        except ModuleNotFoundError:
            spec = importlib.util.spec_from_file_location(self.__solution_file.file_name, self.__solution_file.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        function = getattr(module, 'solve')
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, function, *args, **kwargs)
        return result
