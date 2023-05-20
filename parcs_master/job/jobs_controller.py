import asyncio
import aiohttp
import importlib

from parcs_master.job.job import Job


class JobsController:
    def __init__(self):
        self.__jobs = []
        self.__last_id = 0

    async def create_job(self, solution_file, input_file):
        self.__last_id += 1
        self.__jobs.append(Job(self.__last_id, solution_file, input_file))

    async def get_jobs(self):
        return self.__jobs

    @staticmethod
    async def __fetch(session, url, data, job_id):
        async with session.get(url, body={'data': data, 'job_id': job_id}) as response:
            return await response.json()['result']

    async def execute(self, instances):
        job = self.__jobs[0]
        try:
            module = importlib.import_module(job.solution_file.file_name)
        except ModuleNotFoundError:
            spec = importlib.util.spec_from_file_location(job.solution_file.file_name, job.solution_file.file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        solver = module.Solver(instances, job.input_file.file_name)
        data = solver.read_input(job.input_file.file_path)
        chunks = solver.map(data, instances)
        loop = asyncio.get_running_loop()
        tasks = []
        async with aiohttp.ClientSession(loop=loop) as session:
            for i in range(len(instances)):
                task = asyncio.ensure_future(self.__fetch(session, instances[i].execute_url, chunks[i], job.job_id))
                tasks.append(task)
        results = await asyncio.gather(*tasks)
        result = module.reduce(results)
        return result
