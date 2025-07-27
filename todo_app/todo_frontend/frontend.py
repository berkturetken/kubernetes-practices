from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.request
import base64
import time
import sys
import json

IS_LOCAL = "--local" in sys.argv

if IS_LOCAL:
    CACHE_FILE = "./todo_app/todo_frontend/picsum_image.jpg"
    BACKEND_URL = "http://localhost:8090"
else:
    CACHE_FILE = "/app/files/picsum_image.jpg"
    BACKEND_URL = "http://todo-backend-svc:5678"

CACHE_TIME = 600 # 10 minutes
PORT = int(os.environ.get("PORT", 8080))

def get_image():
    # Check if cache file exists and is fresh
    try:
        if os.path.exists(CACHE_FILE):
            mtime = os.path.getmtime(CACHE_FILE)
            if time.time() - mtime < CACHE_TIME:
                with open(CACHE_FILE, "rb") as f:
                    return f.read()
        # Otherwise, fetch new image and cache it
        with urllib.request.urlopen("https://picsum.photos/1200") as response:
            img_data = response.read()
        with open(CACHE_FILE, "wb") as f:
            f.write(img_data)
        return img_data
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

def fetch_todos():
    try:
        with urllib.request.urlopen(f"{BACKEND_URL}/todos") as response:
            # Parse JSON array from backend
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return ["Could not fetch todos."]

def prepare_basic_html(img_html, todos_html):
    return f"""
            <html>
                <head>
                    <title>ToDo App</title>
                    <style>
                        .todo-input {{ width: 400px; }}
                        .todo-list {{ margin-top: 20px; }}
                    </style>
                </head>
                <body>
                    <h1>Welcome to the ToDo App!</h1>
                    <p>This is a simple HTML page served at the root URL.</p>
                    {img_html}
                    <p><i>The image is refreshed every 10 minutes.</i></p>
                    <hr>
                    <div>
                        <form action="/todos" method="post">
                            <input name="todo" class="todo-input" type="text" maxlength="140" placeholder="Enter your todo (max 140 chars)">
                            <button type="submit">Send</button>
                        </form>
                    </div>
                    <div class="todo-list">
                        <h3>Todos:</h3>
                        <ul>
                            {todos_html}
                        </ul>
                    </div>
                </body>
            </html>
            """

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            img_data = get_image()
            if img_data is not None:
                # Encode image as base64 to embed in HTML
                img_base64 = base64.b64encode(img_data).decode("utf-8")
                img_html = f'<img src="data:image/jpeg;base64,{img_base64}" width="600"/>'
            else:
                img_html = '<p>Error loading image.</p>'
            todos = fetch_todos()
            if len(todos) == 1 and todos[0] == "No todos yet.":
                todos[0] = ""
            todos_html = "".join(f"<li>{todo}</li>" for todo in todos)

            html = prepare_basic_html(img_html, todos_html)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')
    
    def do_POST(self):
        if self.path == '/todos':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            # Forward the POST to the backend
            req = urllib.request.Request(f"{BACKEND_URL}/todos", data=post_data.encode("utf-8"), method="POST")
            req.add_header("Content-Type", "application/x-www-form-urlencoded")
            try:
                with urllib.request.urlopen(req) as resp:
                    # Redirect back to main page after successful POST
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error posting todo: {e}".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Welcome to the ToDo App! Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()