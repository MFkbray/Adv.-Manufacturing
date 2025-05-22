# Advanced Manufacturing Control Panel

A lightweight web application for monitoring and controlling manufacturing equipment over your local network. This application provides a simple interface for tracking machine status, controlling equipment, and managing maintenance schedules.

## Features

- Real-time equipment status monitoring
- Remote control of manufacturing machines
- Maintenance scheduling and tracking
- Production uptime monitoring
- No external services or installations required
- Accessible from any device on the same network

## Requirements
- Python 3.x (which you already have installed)

## How to Run

1. Open a terminal/command prompt
2. Navigate to the project directory
3. Run the following command:
   ```
   python server.py
   ```
4. The server will start and display two URLs:
   - Local URL (for accessing from your computer)
   - WiFi/Network URL (for accessing from other devices on your WiFi network)

## Accessing the Control Panel

- From your computer: Open a web browser and go to `http://localhost:8000`
- From other devices on your WiFi network: 
  1. Make sure the device is connected to the same WiFi network as the computer running the server
  2. Open a web browser
  3. Enter the WiFi/Network URL shown in the terminal (it will look like `http://192.168.x.x:8000`)

## Available API Endpoints

- GET `/api/machine-status`: Returns current status of all machines
- POST `/api/control`: Send control commands to machines

## Machine Control Commands

The following commands are available for each machine:
- Start: Begin machine operation
- Stop: Halt machine operation
- Maintenance: Put machine in maintenance mode

## Security Notes

- The control panel is only accessible to devices connected to the same WiFi network
- Make sure your firewall allows incoming connections on port 8000
- No data is sent to external servers
- If you can't connect from other devices, check your computer's firewall settings

## Future Enhancements

- Real machine integration via industrial protocols
- Historical data logging and analytics
- User authentication and access control
- Custom machine configuration options
- Production scheduling interface 