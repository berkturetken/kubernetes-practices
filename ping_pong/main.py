from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 9100))

pong = 0

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global pong
        if self.path == '/pingpong':
            response = f"pong {pong}"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
            pong += 1
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Welcome to the Ping Pong App! Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()