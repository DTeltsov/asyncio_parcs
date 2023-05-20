from aiohttp import web

from parcs_node.api.views import solution_file_view, execute_view


def init_routes(app):
    app.add_routes([
        web.post('/api/file/', solution_file_view),
        web.get('/api/execute/', execute_view),
    ])
