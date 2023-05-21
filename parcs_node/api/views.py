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


async def execute_view(request):
    json_body = await request.json()
    args = json_body['data'].get('args', ())
    kwargs = json_body['data'].get('kwargs', {})
    job = await request.app['job_controller'].get_job_by_id(json_body['job_id'])
    result = await job.register_methods(args, kwargs)
    return web.json_response({'result': result}, status=200)
