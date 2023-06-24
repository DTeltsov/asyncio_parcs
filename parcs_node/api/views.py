from aiohttp import web
from collections import namedtuple

File = namedtuple('File', ['file_name', 'file_path'])


async def upload_file_view(request):
    data = await request.post()
    job_id = data.get('job_id')
    field = data.get('file')
    filename = field.filename
    file = File(filename, filename)
    with open(filename, 'wb') as f:
        f.write(field.file.read())
    job = await request.app['job_controller'].create_job(job_id, file)
    methods = await job.register_methods(request.app['rpc'])
    return web.json_response({'detail': 'file uploaded', "methods": methods}, status=201)
