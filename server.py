import serial
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS

latest_distance = None
latest_strength = None

@app.route('/send-drone-height', methods=['POST'])
def receive_drone_height():
    global latest_distance
    distance = request.form.get('distance')
    if distance:
        latest_distance = distance
        print(f"Received drone height: {distance} cm")
        return {"message": "Drone height received successfully"}, 200
    else:
        return {"error": "No distance data received"}, 400

@app.route('/send-drone-height', methods=['GET'])
def get_drone_height():
    if latest_distance is not None:
        return jsonify({"distance": latest_distance}), 200
    else:
        return {"error": "No distance data available"}, 404

@app.route('/send-mine-detection', methods=['POST'])
def receive_mine_detection():
    global latest_strength
    strength = request.form.get('strength')
    if strength:
        latest_strength = strength
        print(f"Received metal strength: {strength}")
        return {"message": "Metal strength received successfully"}, 200
    else:
        return {"error": "No strength data received"}, 400

@app.route('/send-mine-detection', methods=['GET'])
def get_mine_detection():
    if latest_strength is not None:
        return jsonify({"strength": latest_strength}), 200
    else:
        return {"error": "No strength data available"}, 404

def read_serial():
    while True:
        if ser and ser.is_open:
            try:
                if ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if "Distance:" in line:
                        parts = line.split("|")
                        distance = parts[0].split(":")[1].strip().split()[0]
                        strength = parts[1].split(":")[1].strip()
                        print(f"Received distance: {distance} cm, strength: {strength}")
                        send_to_server(distance, strength)
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(1)

def send_to_server(distance, strength):
    try:
        response = requests.post('http://localhost:5000/send-drone-height', data={'distance': distance})
        print(f"Server response (distance): {response.status_code}, {response.text}")
        response = requests.post('http://localhost:5000/send-mine-detection', data={'strength': strength})
        print(f"Server response (strength): {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to send data to server: {e}")

if __name__ == '__main__':
    # Attempt to set up serial connection
    try:
        ser = serial.Serial('COM3', 115200)  # Replace 'COM3' with your serial port
        print("Serial port opened successfully")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        ser = None

    if ser:
        # Start the serial reading in a separate thread
        serial_thread = threading.Thread(target=read_serial)
        serial_thread.daemon = True
        serial_thread.start()
    else:
        print("Serial port not available. Ensure the port is correct and not in use by another application.")

    # Start the Flask server
    app.run(debug=True, port=5000)
