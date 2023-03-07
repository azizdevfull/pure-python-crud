from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {"id": 1, "name": "Robinzon Kruzo", "genre": "Tragedia", "author": "Daniel Defo", "price": 45}
]

class Books(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())






if __name__ == '__main__':
    print("men ishladim")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Books)
    httpd.serve_forever()