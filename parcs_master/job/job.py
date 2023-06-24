import asyncio
import importlib
from collections import namedtuple

import aiohttp

File = namedtuple('File', ['file_name', 'file_path'])


class Job:
    def __init__(self, job_id, solution_file: File, input_file: File):
        self.job_id = job_id
        self.solution_file = solution_file
        self.input_file = input_file
        self.status = 'Created'

    async def execute(self, instances):
        self.status = 'Executing'
        try:
            module = importlib.import_module(self.solution_file.file_name)
        except ModuleNotFoundError:
            spec = importlib.util.spec_from_file_location(self.solution_file.file_name, self.solution_file.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        solver = module.Solver(instances, self.input_file.file_name)
        try:
            await solver.solve()
            self.status = 'Success'
        except Exception as e:
            self.status = 'Error'

