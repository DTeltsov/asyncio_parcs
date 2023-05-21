import pathlib
from .views import *


def init_routes(app):
    app.add_routes([
        web.get('/', instances_view),
        web.get('/instances/', instances_view),
        web.get('/instances/create/', add_instance_view),
        web.get('/instances/delete/', remove_instance_view),
        web.get('/add_job/', add_job_view),
        web.post('/add_job/', add_job_view),
        web.get('/jobs/', get_jobs_view)
    ])

    app.router.add_static(
        '/static/',
        path=(pathlib.Path(__file__).parent / 'static'),
        name='static',
    )
