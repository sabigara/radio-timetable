import http.server
import socketserver

PORT = 8000
DIRECTORY = "server"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)


def serve():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("Serving at port", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Keyboard interrupt.")
