from .job import Job


class JobsController:
    def __init__(self):
        self.__jobs = []
        self.__last_id = 0

    async def create_job(self, solution_file, input_file):
        self.__last_id += 1
        job = Job(self.__last_id, solution_file, input_file)
        self.__jobs.append(Job(self.__last_id, solution_file, input_file))
        return job

    async def get_jobs(self):
        return self.__jobs

    async def get_id(self):
        return self.__last_id + 1
