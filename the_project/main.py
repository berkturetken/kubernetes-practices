from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 8080))

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, World!\n')

if __name__ == "__main__":
    print(f"Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()