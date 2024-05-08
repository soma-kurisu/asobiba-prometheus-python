import http.server
import random
import time
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram

REQUESTS = Counter('hello_worlds_total', 'Hello Worlds requested.')
SALES = Counter('hello_world_sales_euro_total', 'Euros made serving Hello World.')
EXCEPTIONS = Counter('hello_world_exceptions_total', 'Exceptions serving Hello World.')

INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')
TIME = Gauge('time_seconds', 'The current time.')
TIME.set_function(lambda: time.time())

LATENCY_SUMMARY = Summary('hello_world_latency_summary_seconds', 'Time for a request Hello World.')

LATENCY_HISTOGRAM = Histogram(
    'hello_world_latency_histogram_seconds', 
    'Time for a request Hello World.', 
    buckets=[0.1 * 2**x for x in range(1, 10)]) # Exponential

class MyHandler(http.server.BaseHTTPRequestHandler):
    @EXCEPTIONS.count_exceptions()
    @INPROGRESS.track_inprogress()
    @LATENCY_SUMMARY.time()
    @LATENCY_HISTOGRAM.time()
    def do_GET(self):
        REQUESTS.inc()
        # INPROGRESS.inc()
        # start = time.time()

        # with EXCEPTIONS.count_exceptions():
        if random.random() < 0.1:
            raise Exception
        elif random.random() < 0.1:
            self.send_response(301)
            self.wfile.write(b"Ups moved!")
        elif random.random() < 0.1:
            self.send_response(400)
            self.wfile.write(b"Ups bad request!")
        elif random.random() < 0.1:
            self.send_response(401)
            self.wfile.write(b"Ups unauthorized!")
        elif random.random() < 0.1:
            self.send_response(403)
            self.wfile.write(b"Ups forbidden!")
        elif random.random() < 0.1:
            self.send_response(404)
            self.wfile.write(b"Ups not found!")
        elif random.random() < 0.1:
            self.send_response(500)
            self.wfile.write(b"Panic!")
        
        euros = random.getrandbits(6) + random.random()
        SALES.inc(euros)

        if random.random() < 0.3:
            self.send_response(202)
            self.end_headers()
            self.wfile.write(b"Hello World Accepted")
        elif random.random() < 0.3:
            self.send_response(201)
            self.end_headers()
            self.wfile.write(b"Hello World Created")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Hello World OK")

        # LAST.set(time.time())
        # LATENCY.observe(time.time() - start)
        INPROGRESS.dec()

if __name__ == "__main__":
    start_http_server(8000)
    server = http.server.HTTPServer(('localhost', 8001), MyHandler)
    server.serve_forever()