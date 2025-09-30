from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from db import get_transaction, add_transaction, update_transaction, delete_transaction, load_transactions

USERNAME = "admin"
PASSWORD = "password"

def check_auth(headers):
    auth = headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        return False
    import base64
    encoded = auth.split(" ")[1]
    decoded = base64.b64decode(encoded).decode()
    user, pwd = decoded.split(":")
    return user == USERNAME and pwd == PASSWORD

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def _unauthorized(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", "Basic realm='API'")
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())

    def do_GET(self):
        if not check_auth(self.headers):
            return self._unauthorized()
        if self.path == "/transactions":
            self._set_headers()
            self.wfile.write(json.dumps(load_transactions()).encode())
        elif self.path.startswith("/transactions/"):
            tid = self.path.split("/")[-1]
            tx = get_transaction(tid)
            if tx:
                self._set_headers()
                self.wfile.write(json.dumps(tx).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

    def do_POST(self):
        if not check_auth(self.headers):
            return self._unauthorized()
        if self.path == "/transactions":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            new_tx = add_transaction(data)
            self._set_headers(201)
            self.wfile.write(json.dumps(new_tx).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

    def do_PUT(self):
        if not check_auth(self.headers):
            return self._unauthorized()
        if self.path.startswith("/transactions/"):
            tid = self.path.split("/")[-1]
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode())
            updated = update_transaction(tid, data)
            if updated:
                self._set_headers()
                self.wfile.write(json.dumps(updated).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

    def do_DELETE(self):
        if not check_auth(self.headers):
            return self._unauthorized()
        if self.path.startswith("/transactions/"):
            tid = self.path.split("/")[-1]
            deleted = delete_transaction(tid)
            if deleted:
                self._set_headers()
                self.wfile.write(json.dumps({"message": "Transaction deleted"}).encode())
            else:
                self._set_headers(404)
                self.wfile.write(json.dumps({"error": "Transaction not found"}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Invalid endpoint"}).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"🚀 Server running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()

