from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import random
import string
import os


PORT = int(os.environ.get("PORT", 9000))

results = []

def generate_result():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    iso_timestamp = datetime.now().isoformat()
    return f"{iso_timestamp}: {random_string}"

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/generate-output':
            new_result = generate_result()
            results.append(new_result)

            # Keep only the last 20 results
            if len(results) > 20:
                del results[0:len(results)-20]
            print(results)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            results_html = "<br>".join(results)
            html = f"""
            <html>
                <head>
                    <title>Log Output App</title>
                    <meta http-equiv="refresh" content="5">
                </head>
                <body>
                    <h1>Welcome to the Log Output App!</h1>
                    <p><b>Results (latest at bottom):</b></p>
                    <div style="font-family:monospace;">{results_html}</div>
                    <p><i>This page refreshes every 5 seconds and keeps the last 20 results.</i></p>
                </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found\n')

if __name__ == "__main__":
    httpd = HTTPServer(("", PORT), SimpleHandler)
    httpd.serve_forever()
