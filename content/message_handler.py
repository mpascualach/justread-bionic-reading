from http.server import HTTPServer, BaseHTTPRequestHandler

class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        message = self.rfile.read(content_length).decode('utf-8')

        if message == 'opened':
            print("Output file has already been opened!")

        self.send_respone(200)
        self.end_headers()

def start_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    print("Listening...")
    httpd.serve_forever()

if __name__ == '__main__':
    start_server()