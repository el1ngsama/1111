from http.server import BaseHTTPRequestHandler
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path.startswith('/api/'):
            path = path[4:]
        
        with app.test_client() as client:
            response = client.get(path)
            
            self.send_response(response.status_code)
            for key, value in response.headers:
                if key.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.data)
    
    def do_POST(self):
        path = self.path
        if path.startswith('/api/'):
            path = path[4:]
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        with app.test_client() as client:
            response = client.post(
                path,
                data=post_data,
                content_type=self.headers.get('Content-Type', 'application/json')
            )
            
            self.send_response(response.status_code)
            for key, value in response.headers:
                if key.lower() not in ['content-length', 'transfer-encoding']:
                    self.send_header(key, value)
            self.end_headers()
            self.wfile.write(response.data)
