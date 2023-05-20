from parcs_node.job.job import Job


class JobsController:
    def __init__(self):
        self.__jobs = []

    async def create_job(self, job_id, solution_file):
        self.__jobs.append(Job(job_id, solution_file))

    async def get_job_by_id(self, job_id):
        return [job for job in self.__jobs if job.id == job_id][0]
