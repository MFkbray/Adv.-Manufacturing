from flask import Flask, send_file, jsonify, request
from pyngrok import ngrok
import json
import os

app = Flask(__name__)

# Mock data for machine status
MACHINE_STATUS = {
    'machines': [
        {'id': 1, 'name': 'CNC Machine 1', 'status': 'Running', 'uptime': '12h 30m'},
        {'id': 2, 'name': 'Assembly Line A', 'status': 'Idle', 'uptime': '8h 45m'},
        {'id': 3, 'name': '3D Printer', 'status': 'Maintenance', 'uptime': '0h'}
    ]
}

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/api/machine-status')
def machine_status():
    return jsonify(MACHINE_STATUS)

@app.route('/api/control', methods=['POST'])
def control_machine():
    command = request.json
    response = {
        'status': 'success',
        'message': f"Command '{command.get('action', '')}' sent to machine {command.get('machine_id', '')}"
    }
    return jsonify(response)

def run_app():
    try:
        # Start ngrok tunnel
        port = 5000
        # Enable Flask development mode
        os.environ['FLASK_ENV'] = 'development'
        
        # Start ngrok tunnel with specific options
        public_url = ngrok.connect(port, bind_tls=True).public_url
        
        print("\nAdvanced Manufacturing Web App Server running at:")
        print(f"- Local: http://localhost:{port}")
        print(f"- Public URL (accessible from anywhere): {public_url}")
        print("\nShare the Public URL with others to access the application")
        print("\nPress Ctrl+C to stop the server")
        
        # Run the Flask app with specific host and port
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure port 5000 is not in use")
        print("2. Try running with a different port:")
        print("   Example: Change port = 5000 to port = 3000")
        print("3. Check your internet connection")
        
    finally:
        # Disconnect ngrok on exit
        try:
            ngrok.disconnect(public_url)
        except:
            pass

if __name__ == '__main__':
    run_app() 