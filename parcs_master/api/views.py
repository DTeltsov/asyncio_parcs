import asyncio
import json
from collections import namedtuple

from aiohttp import web, ClientSession, FormData
from aiohttp_jinja2 import template
from parcs_master.cloud.instance import Instance
from aiohttp_rpc import JsonRpcClient

File = namedtuple('File', ['file_name', 'file_path'])


@template('instances.html')
async def instances_view(request):
    instances = await request.app['cloud_controller'].get_instances()
    return {'instances': instances}


async def send_data(url, file_path, json_data):
    async with ClientSession() as session:
        data = FormData()
        data.add_field('file', open(file_path, 'rb'))
        data.add_field('json', json.dumps(json_data), content_type='application/json')

        async with session.post(url, data=data) as response:
            print(f"Response from {url}: {response.status}")


async def upload_files(request, job_id):
    reader = await request.multipart()
    files = []
    for i in range(2):
        field = await reader.next()
        filename = field.filename.split('.')
        filename[0] = f"{filename[0]}_job_{job_id}"
        filename = '.'.join(filename)
        files.append(File(filename, filename))
        with open(filename, 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
    return files


@template('add_job.html')
async def add_job_view(request):
    if request.method == 'POST':
        job_id = await request.app['jobs_controller'].get_id()
        files = await upload_files(request, job_id)
        job = await request.app['jobs_controller'].create_job(files[0], files[1])
        # instances = await request.app['cloud_controller'].get_instances()
        instances = [Instance()]
        tasks = []
        for instance in instances:
            task = send_data(instance.upload_url, files[0].file_path, {"job_id": job_id})
            tasks.append(task)
        await asyncio.gather(*tasks)
        async with ClientSession() as session:
            bad_result = await job.execute([JsonRpcClient(instance.rpc, session=session) for instance in instances])
        print(bad_result)
        return web.HTTPFound('/jobs/')
    elif request.method == 'GET':
        return {}


@template('jobs.html')
async def get_jobs_view(request):
    jobs = await request.app['jobs_controller'].get_jobs()
    return {'jobs': jobs}


async def add_instance_view(request):
    await request.app['cloud_controller'].create_instance()
    return web.HTTPFound('/instances/')


async def remove_instance_view(request):
    name = request.query['name']
    await request.app['cloud_controller'].delete_instance(name)
    return web.HTTPFound('/instances/')
