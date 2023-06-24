from aiohttp import web
from aiohttp_rpc import rpc_server
from .views import upload_file_view


def init_routes(app):
    app.add_routes([
        web.post('/api/upload/', upload_file_view),
        web.post('/rpc/', rpc_server.handle_http_request)
    ])
