from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import psycopg2
from dotenv import load_dotenv
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
    print("You hit the db conn function.")
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
    cur.execute("CREATE TABLE IF NOT EXISTS pong_counter (id SERIAL PRIMARY KEY, count INTEGER);")
    cur.execute("SELECT count(*) FROM pong_counter;")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO pong_counter (count) VALUES (0);")
    conn.commit()
    cur.close()
    conn.close()

def get_pong():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT count FROM pong_counter WHERE id=1;")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else 0

def increment_pong():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("UPDATE pong_counter SET count = count + 1 WHERE id=1;")
    conn.commit()
    cur.close()
    conn.close()

init_db()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global pong
        if self.path == '/pingpong':
            increment_pong()
            response = "Executed successfully."
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))
        elif self.path == '/pings':
            pong = get_pong()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(pong).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    if IS_LOCAL:
        print(f"Welcome to the Ping Pong App! Starting server on port {PORT}...")
    else:
        print(f"Welcome to the Ping Pong App! Starting server in a Kubernetes cluster on port 8081...")
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()