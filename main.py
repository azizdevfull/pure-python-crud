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
        elif self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            
            for item in data:
                if item['id'] == book_id:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(item).encode())
                    break
            else:
                self.send_error(404)
        else:
            self.send_error(404)
            
    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data.decode())
            new_item['id'] = len(data) + 1
            data.append(new_item)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Location', '/data/{}'.format(new_item['id']))
            self.end_headers()
            self.wfile.write(json.dumps(new_item).encode())
        else:
            self.send_error(404)        






if __name__ == '__main__':
    print("men ishladim")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Books)
    httpd.serve_forever()