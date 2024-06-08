from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

drone_height = 0
last_coordinates = {'latitude': 0.0, 'longitude': 0.0}
flight_time = 0

@app.route('/send-drone-height', methods=['GET', 'POST'])
def handle_drone_height():
    global drone_height
    if request.method == 'POST':
        data = request.json
        drone_height = data.get('drone_height', 0)
        print(f"Received drone height: {drone_height} cm")
        return jsonify({'message': 'Height received', 'drone_height': drone_height}), 200
    else:
        return jsonify({'drone_height': drone_height}), 200

@app.route('/send-coordinates', methods=['GET', 'POST'])
def handle_coordinates():
    global last_coordinates
    if request.method == 'POST':
        data = request.json
        last_coordinates['latitude'] = data.get('latitude', 0.0)
        last_coordinates['longitude'] = data.get('longitude', 0.0)
        print(f"Received coordinates: {last_coordinates}")
        return jsonify({'message': 'Coordinates received', 'coordinates': last_coordinates}), 200
    else:
        return jsonify({'coordinates': last_coordinates}), 200

@app.route('/send-flight-time', methods=['POST'])
def handle_flight_time():
    global flight_time
    data = request.json
    flight_time = data.get('flight_time', 0)
    print(f"Received flight time: {flight_time} seconds")
    return jsonify({'message': 'Flight time received', 'flight_time': flight_time}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)