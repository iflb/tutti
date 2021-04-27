from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import subprocess
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] [%(levelname)s] %(message)s')
logger = logging.getLogger()

prj_hashes = {}

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        # returns if the queried project has been changed
        self._set_response()
        prj_name = self.path.split("/")[1]

        try:
            p1 = subprocess.run(["tar","-c","projects/{}".format(prj_name)], check=True, capture_output=True)
            p2 = subprocess.run(["shasum"], input=p1.stdout, capture_output=True)
            hash_val = p2.stdout[:10]

            if check_prj_hash_diff(prj_name, hash_val):
                self.wfile.write(b"1")
            else:
                self.wfile.write(b"0")

        except subprocess.CalledProcessError as e:
            self.wfile.write(b"-1")

    def do_POST(self):
        # rebuilds production environments
        self._set_response()
        prj_name = self.path.split("/")[1]

        p1 = subprocess.run(["tar","-c","projects/{}".format(prj_name)], check=True, capture_output=True)
        p2 = subprocess.run(["shasum"], input=p1.stdout, capture_output=True)
        hash_val = p2.stdout[:10]
        prj_hashes[prj_name] = hash_val

        subprocess.run(["docker-compose", "restart", "backend"])
        subprocess.run(["docker-compose", "up", "frontend"])

        self.wfile.write(b"1")

def check_prj_hash_diff(prj_name, hash_val):
    return (prj_name not in prj_hashes) or (prj_hashes[prj_name]!=hash_val)

def run(server_class=HTTPServer, handler_class=S, port=18080):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    logger.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logger.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
