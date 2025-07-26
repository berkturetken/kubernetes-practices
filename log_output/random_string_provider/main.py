from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 9000))

# For testing
# OUTPUT_FILE = "./log_output/random_string_generator/output.log"

# For production
OUTPUT_FILE = "/usr/src/app/files/output.log"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                with open(OUTPUT_FILE, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                content = "No log file found."

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Random String Provider running on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()