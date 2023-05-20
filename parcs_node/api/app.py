import socket
from aiohttp import web

from parcs_node.api.routes import init_routes
from parcs_node.job import JobsController


def create_app():
    app = web.Application()
    app['job_controller'] = JobsController()
    init_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    hostname = socket.gethostname()
    web.run_app(app, host=socket.gethostbyname(hostname))
