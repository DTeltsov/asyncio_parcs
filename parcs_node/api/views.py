from aiohttp import web
from parcs_node.job import File


async def solution_file_view(request):
    job_id = await request.json()['job_id']
    reader = await request.multipart()
    field = await reader.next()
    filename = field.filename
    file = File(filename, filename)
    with open(filename, 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            f.write(chunk)
    request.app['job_controller'].create_job(job_id, file)
    return web.json_response({'detail': 'file uploaded'}, status=201)


async def execute_view(request):
    json_body = await request.json()
    data = json_body['data']
    job = request.app['job_controller'].get_job_by_id(json_body['job_id'])
    result = await job.execute(data)
    return web.json_response({'result': result}, status=200)
