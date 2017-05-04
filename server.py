import web
import socketserver
PORT = 8000
Handler = web.testHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
socketserver.TCPServer.allow_resue_address=True
