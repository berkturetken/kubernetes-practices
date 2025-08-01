from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv
import os
from urllib.parse import parse_qs
import json
import psycopg2
import sys


load_dotenv()
PORT = int(os.environ.get("PORT"))
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = int(os.environ.get("POSTGRES_PORT"))

IS_LOCAL = "--local" in sys.argv
if IS_LOCAL:
    HOST= os.environ.get("LOCAL_POSTGRES_HOST")
else:
    HOST = os.environ.get("PROD_POSTGRES_HOST")

def get_db_conn():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=HOST,
        port=DB_PORT
    )

def init_db():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todos (id SERIAL PRIMARY KEY, content VARCHAR(140) NOT NULL);")
    conn.commit()
    cur.close()
    conn.close()

# Initialize the database
init_db()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/todos':
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                cur.execute("SELECT content FROM todos;")
                todos = [row[0] for row in cur.fetchall()] 
                if not todos:
                    todos = ["No todos yet."]
                response = json.dumps(todos)
                cur.close()
                conn.close()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                print(f"Error: {str(e)}")
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}\n'.encode("utf-8"))
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
                try:
                    conn = get_db_conn()
                    cur = conn.cursor()
                    cur.execute("INSERT INTO todos (content) VALUES (%s);", (todo,))
                    conn.commit()
                    cur.close()
                    conn.close()

                    self.send_response(201)
                    self.end_headers()
                except Exception as e:
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(f"Database error: {str(e)}".encode("utf-8"))
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