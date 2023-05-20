from collections import namedtuple

File = namedtuple('File', ['file_name', 'file_path'])


class Job:
    def __init__(self, job_id, solution_file: File, input_file: File):
        self.job_id = job_id
        self.solution_file = solution_file
        self.input_file = input_file
        self.status = 'Done'
