import http.server
import socketserver
import sys

PORT = 5002

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        sys.stdout.flush()
        httpd.serve_forever()
except Exception as e:
    print(f"Error: {e}")
    sys.stdout.flush()
