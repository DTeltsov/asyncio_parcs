import argparse
import sys
from pathlib import Path

import aiohttp_jinja2
import jinja2
from aiohttp import web

from api.routes import init_routes
from cloud import GoogleCloudController
from job import JobsController


def init_jinja2(app) -> None:
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(str(Path(__file__).parent / 'api/templates'))
    )


def create_app(creds):
    app = web.Application()
    app['cloud_controller'] = GoogleCloudController(creds=creds)
    app['jobs_controller'] = JobsController()
    init_routes(app)
    init_jinja2(app)
    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-cc", '--cloud_creds', help="path to google cloud credentials json file")
    argv, unknown = parser.parse_known_args()
    if not argv.cloud_creds:
        print('Please, provide path to your google cloud credentials json file')
        sys.exit(0)

    app = create_app(creds=argv.cloud_creds)
    web.run_app(app)
