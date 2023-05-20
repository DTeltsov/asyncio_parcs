import pathlib

from aiohttp import web

from parcs_master.api.views import add_instance_view, instances_view, \
    remove_instance_view, add_job_view, get_jobs_view


def init_routes(app):
    app.add_routes([
        web.get('/', instances_view),
        web.get('/instances/', instances_view),
        web.get('/instances/create/', add_instance_view),
        web.get('/instances/delete/', remove_instance_view),
        web.get('/add_job/', add_job_view),
        web.post('/add_job/', add_job_view),
        web.get('/jobs/', get_jobs_view),
    ])

    app.router.add_static(
        '/static/',
        path=(pathlib.Path(__file__).parent / 'static'),
        name='static',
    )
