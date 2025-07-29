from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import os
from urllib.parse import parse_qs
import json


load_dotenv()
PORT = int(os.environ.get("PORT"))
todos = []


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/todos':
            response = json.dumps(todos)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')
    
    def do_POST(self):
        if self.path == '/todos':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            # Parse form data (application/x-www-form-urlencoded)
            form = parse_qs(post_data)
            todo = form.get("todo", [""])[0]
            if 0 < len(todo) <= 140:
                todos.append(todo)
                self.send_response(201)
                self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Todo must be 1-140 characters long.\n')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Backend of the ToDo App! Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()