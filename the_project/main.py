from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import urllib.request
import base64
import time


# For testing:
# CACHE_FILE = "./the_project/picsum_image.jpg"
# For production:
CACHE_FILE = "/app/files/picsum_image.jpg"

CACHE_TIME = 600 # 10 minutes
PORT = int(os.environ.get("PORT", 8080))

def get_image():
    # Check if cache file exists and is fresh
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

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            try:
                img_data = get_image()
                # Encode image as base64 to embed in HTML
                img_base64 = base64.b64encode(img_data).decode("utf-8")
                img_html = f'<img src="data:image/jpeg;base64,{img_base64}" width="600"/>'

                # Hardcoded todos
                todos = [
                    "Buy groceries",
                    "Finish Kubernetes course",
                    "Read a book"
                ]
                todos_html = "".join(f"<li>{todo}</li>" for todo in todos)

                html = f"""
                <html>
                    <head>
                        <title>ToDo App</title>
                        <style>
                            .todo-input {{ width: 400px; }}
                            .todo-list {{ margin-top: 20px; }}
                        </style>
                        <script>
                        function checkLength(input) {{
                            if (input.value.length > 140) {{
                                input.value = input.value.slice(0, 140);
                                document.getElementById('char-warning').style.display = 'block';
                            }} else {{
                                document.getElementById('char-warning').style.display = 'none';
                            }}
                        }}
                        </script>
                    </head>
                    <body>
                        <h1>Welcome to the ToDo App!</h1>
                        <p>This is a simple HTML page served at the root URL.</p>
                        {img_html}
                        <p><i>The image is refreshed every 10 minutes.</i></p>
                        <hr>
                        <div>
                            <input class="todo-input" type="text" maxlength="140" placeholder="Enter your todo (max 140 chars)" oninput="checkLength(this)">
                            <button>Send</button>
                            <div id="char-warning" style="color:red;display:none;">Todo cannot be longer than 140 characters!</div>
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
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error fetching image: {e}".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    print(f"Welcome to the ToDo App! Starting server on port {PORT}...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()