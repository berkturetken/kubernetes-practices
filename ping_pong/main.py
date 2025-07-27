from http.server import HTTPServer, BaseHTTPRequestHandler
import os

PORT = int(os.environ.get("PORT", 9100))

pong = 0

# For testing
# OUTPUT_DIR = "./log_output/random_string_generator"

# For production
# OUTPUT_DIR = "/usr/src/app/files"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# OUTPUT_FILE = os.path.join(OUTPUT_DIR, "output.log")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global pong
        if self.path == '/pingpong':
            # with open(OUTPUT_FILE, "a") as f:
            #     f.write(f"Ping / Pongs: {pong}\n")
            response = "Executed successfully."
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
            pong += 1
        elif self.path == '/pings':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(pong).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Welcome to the Ping Pong App! Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()