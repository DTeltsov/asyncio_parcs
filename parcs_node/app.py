import socket
from aiohttp import web
from aiohttp_rpc import rpc_server

from api.routes import init_routes
from job import JobsController


def create_app():
    app = web.Application()
    app['job_controller'] = JobsController()
    app['rpc'] = rpc_server
    init_routes(app)
    return app


if __name__ == '__main__':
    app = create_app()
    hostname = socket.gethostname()
    web.run_app(app, host=socket.gethostbyname(hostname))
