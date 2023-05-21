import importlib
from collections import namedtuple
from inspect import getmembers, isroutine

File = namedtuple('File', ['file_name', 'file_path'])


class Job:
    def __init__(self, job_id, solution_file: File):
        self.id = job_id
        self.__solution_file = solution_file

    async def register_methods(self, rpc_server):
        try:
            module = importlib.import_module(self.__solution_file.file_name)
        except ModuleNotFoundError:
            spec = importlib.util.spec_from_file_location(
                self.__solution_file.file_name,
                self.__solution_file.file_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        solver = module.Solver()
        if not (methods := [method[1] for method in getmembers(solver, isroutine) if not method[0].startswith('_')]):
            return 'No methods detected'
        rpc_server.add_methods(methods, replace=True)
        return rpc_server.get_methods()
