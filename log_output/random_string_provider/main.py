from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import sys


PORT = int(os.environ.get("PORT", 9000))
MESSAGE = os.environ.get("MESSAGE", "No MESSAGE env variable set.")
print(f"MESSAGE from env: {MESSAGE}")

IS_LOCAL = "--local" in sys.argv
if IS_LOCAL: # local
    OUTPUT_FILE = "./log_output/random_string_generator/output.log"
    INFO_FILE = "./log_output/random_string_provider/information.txt"
else: # production
    OUTPUT_FILE = "/usr/src/app/files/output.log"
    INFO_FILE = "/usr/src/app/info/information.txt"

if os.path.exists(INFO_FILE):
    with open(INFO_FILE) as f:
        info_content = f.read()
    print(f"information.txt content:\n{info_content}")
else:
    print("information.txt not found.")


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            content = f"file content: {info_content}env variable: MESSAGE={MESSAGE}\n\n"
            try:
                with open(OUTPUT_FILE, "r") as f:
                    content += f.read()
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