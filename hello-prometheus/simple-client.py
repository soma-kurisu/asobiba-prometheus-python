import http.server
import random
from prometheus_client import start_http_server
from prometheus_client import Counter

REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')
SALES = Counter('hello_world_sales_euro_total', 'Euros made serving Hello World.')
EXCEPTIONS = Counter('hello_world_exceptions_total', 'Exceptions serving Hello World.')

class MyHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()  # Decorate the handler with the exception counter.
    def do_GET(self):
        REQUESTS.inc()
        # with EXCEPTIONS.count_exceptions():
        if random.random() < 0.2:
            raise Exception
        
        euros = random.getrandbits(6) + random.random()
        SALES.inc(euros)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()