from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Books(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            with open('books.json') as f:
                data = json.load(f)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        elif self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            with open('books.json') as f:
                data = json.load(f)
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
            with open('books.json') as f:
                data = json.load(f)
            new_item['id'] = len(data) + 1
            data.append(new_item)
            with open('books.json', 'w') as f:
                json.dump(data, f)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Location', '/books/{}'.format(new_item['id']))
            self.end_headers()
            self.wfile.write(json.dumps(new_item).encode())
        else:
            self.send_error(404)        

    def do_PUT(self):
        if self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            content_length = int(self.headers['Content-Length'])
            put_data = self.rfile.read(content_length)
            updated_item = json.loads(put_data.decode())
            with open('books.json') as f:
                data = json.load(f)
            for i, item in enumerate(data):
                if item['id'] == book_id:
                    updated_item['id'] = book_id
                    data[i] = updated_item
                    with open('books.json', 'w') as f:
                        json.dump(data, f)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(updated_item).encode())
                    break
            else:
                self.send_error(404)
        else:
            self.send_error(404)
            
    def do_DELETE(self):
        if self.path.startswith('/books/'):
            book_id = int(self.path.split('/')[-1])
            with open('books.json') as f:
                data = json.load(f)
            for i, item in enumerate(data):
                if item['id'] == book_id:
                    del data[i]
                    with open('books.json', 'w') as f:
                        json.dump(data, f)
                    self.send_response(204)
                    self.end_headers()
                    break
            else:
                self.send_error(404)
        else:
            self.send_error(404)

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, Books)
    print("Server Ishladi")
    httpd.serve_forever()
