import asyncio

from aiohttp import web, ClientSession
from aiohttp_jinja2 import template
from parcs_master.job import File


@template('instances.html')
async def instances_view(request):
    instances = await request.app['cloud_controller'].get_instances()
    return {'instances': instances}


@template('add_job.html')
async def add_job_view(request):
    if request.method == 'POST':
        reader = await request.multipart()
        files = []
        for i in range(2):
            field = await reader.next()
            filename = field.filename
            files.append(File(filename, filename))
            with open(filename, 'wb') as f:
                while True:
                    chunk = await field.read_chunk()
                    if not chunk:
                        break
                    f.write(chunk)
        await request.app['jobs_controller'].create_job(files[0], files[1])
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
