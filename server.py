from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import json
from urllib.parse import parse_qs, urlparse
import os
import sys

class ManufacturingAppHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        
        # Serve the main page
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
            return

        # API endpoint for machine status (mock data)
        elif parsed_path.path == '/api/machine-status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Mock machine status data
            status = {
                'machines': [
                    {'id': 1, 'name': 'CNC Machine 1', 'status': 'Running', 'uptime': '12h 30m'},
                    {'id': 2, 'name': 'Assembly Line A', 'status': 'Idle', 'uptime': '8h 45m'},
                    {'id': 3, 'name': '3D Printer', 'status': 'Maintenance', 'uptime': '0h'}
                ]
            }
            self.wfile.write(json.dumps(status).encode())
            return
            
        # Handle other static files
        return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Parse the URL
        parsed_path = urlparse(self.path)

        # Handle machine control commands
        if parsed_path.path == '/api/control':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            command = json.loads(post_data.decode('utf-8'))

            # Mock response
            response = {
                'status': 'success',
                'message': f"Command '{command.get('action', '')}' sent to machine {command.get('machine_id', '')}"
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return

def get_local_ip():
    try:
        # Get all network interfaces
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        
        # Filter out localhost and try to find the most likely local network IP
        for ip in ip_addresses:
            if not ip.startswith('127.'):
                return ip
                
        # If no other IP is found, try the original method
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Note: Could not determine network IP ({str(e)})")
        return '127.0.0.1'

def try_port(port):
    try:
        server_address = ('0.0.0.0', port)
        httpd = HTTPServer(server_address, ManufacturingAppHandler)
        return httpd
    except Exception as e:
        return None

def run_server():
    # List of ports to try (commonly open ports)
    ports = [8080, 80, 3000, 5000, 8000]
    
    # Try each port until one works
    httpd = None
    used_port = None
    
    for port in ports:
        httpd = try_port(port)
        if httpd:
            used_port = port
            break
    
    if not httpd:
        print("Error: Could not find an available port. Please try running with a specific port:")
        print("Example: python server.py 9000")
        sys.exit(1)

    local_ip = get_local_ip()
    print(f"\nAdvanced Manufacturing Web App Server running at:")
    print(f"- Local: http://localhost:{used_port}")
    print(f"- WiFi/Network: http://{local_ip}:{used_port}")
    print("\nTroubleshooting Tips:")
    print(f"1. Using port {used_port} (commonly open in firewalls)")
    print("2. All devices must be on the same WiFi network")
    print("3. Try accessing the server using any of these IP addresses:")
    
    try:
        hostname = socket.gethostname()
        ip_addresses = socket.gethostbyname_ex(hostname)[2]
        for ip in ip_addresses:
            if ip != local_ip:
                print(f"   - http://{ip}:{used_port}")
    except Exception:
        pass
        
    print("\nPress Ctrl+C to stop the server")
    httpd.serve_forever()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # If port specified as command line argument
        try:
            port = int(sys.argv[1])
            httpd = try_port(port)
            if httpd:
                print(f"\nUsing specified port: {port}")
                run_server()
            else:
                print(f"Error: Could not use port {port}")
                sys.exit(1)
        except ValueError:
            print("Error: Port must be a number")
            sys.exit(1)
    else:
        # Try common ports
        run_server() 