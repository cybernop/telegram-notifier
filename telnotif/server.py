import http.server
import json
import logging
import socketserver

logger = logging.getLogger(__name__)


class Server:
    notifier = None
    routes = {}

    def __init__(self, host='', port=90, notifier=None):

        logger.info(f'start server at {host}:{port}')
        self.server = socketserver.TCPServer((host, port), Server.Handler)
        Server.notifier = notifier

        try:
            Server.routes['/message'] = Server.notifier.send_message
        except AttributeError:
            logger.error('failed to register routes, notifier not set')

    def start(self):
        self.server.serve_forever()

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            status = 404

            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_data = self.rfile.read(content_length)
            post_data = json.loads(post_data)

            try:
                Server.routes[self.path](**post_data)
                status = 201
            except KeyError:
                logger.error(f'route {self.path} not registered')

            self.send_response(status)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            return None


if __name__ == '__main__':
    service = Server(port=9000, notifier=None)
    service.start()
