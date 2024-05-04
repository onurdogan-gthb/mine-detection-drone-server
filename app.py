#   M I N E   D E T E C T I O N   D R O N E   S E R V E R



# IMPORTS
import logging
import random
import requests
import threading
import time
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS



# defining the server
app = Flask(__name__)
api = Api(app)
CORS(app, origins=['http://localhost:3000']) # URL of the UI



# icon
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')



# lock
print_lock = threading.Lock()



# GLOBAL VARIABLES
flight_time = 0
drone_started = False
rotors_states = {}
mine_detected = False
last_coordinates = {}
battery_level = 100



# FUNCTIONS
# Flight Time
def send_flight_time():
    global flight_time
    interval = 1

    url = 'http://127.0.0.1:5000/send-flight-time'
    
    while True:
        try:
            flight_time += interval

            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json={'flight_time': flight_time}, headers=headers)

            with print_lock:
                if response.status_code == 200:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'SUCCESS = ' + '\033[38;2;{r};{g};{b}m'.format(r=128, g=255, b=128) + 'Flight Time' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Value = ' + '\033[0m' + str(flight_time))
                else:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=0) + 'FAILURE = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=128, b=128) + 'Flight Time' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=255, g=192, b=192) + ' Status Code = ' + '\033[0m' + str(response.status_code))
        except Exception as e:
            with print_lock:
                print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=0) + 'ERROR = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=128) + 'Flight Time' + '\033[0m')
                print('\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=192) + ' Exception = ' + '\033[0m' + str(e))
        
        time.sleep(interval)
# Rotors' States
def send_rotors_states():
    global rotors_states
    interval = 1

    url = 'http://127.0.0.1:5000/send-rotors-states'

    while True:
        try:
            rotor_nw_rpm = 1000
            rotor_nw_angle = 0
            rotor_ne_rpm = 1000
            rotor_ne_angle = 0
            rotor_sw_rpm = 1000
            rotor_sw_angle = 0
            rotor_se_rpm = 1000
            rotor_se_angle = 0

            rotor_nw = {'rotor_nw_rpm': rotor_nw_rpm, 'rotor_nw_angle': rotor_nw_angle}
            rotor_ne = {'rotor_ne_rpm': rotor_ne_rpm, 'rotor_ne_angle': rotor_ne_angle}
            rotor_sw = {'rotor_sw_rpm': rotor_sw_rpm, 'rotor_sw_angle': rotor_sw_angle}
            rotor_se = {'rotor_se_rpm': rotor_se_rpm, 'rotor_se_angle': rotor_se_angle}

            rotors_states = {
            'rotor_nw': rotor_nw,
            'rotor_ne': rotor_ne,
            'rotor_sw': rotor_sw,
            'rotor_se': rotor_se
            }

            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=rotors_states, headers=headers)

            with print_lock:
                if response.status_code == 200:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'SUCCESS = ' + '\033[38;2;{r};{g};{b}m'.format(r=128, g=255, b=128) + "Rotors' States" + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Rotor NW')
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  RPM = ' + '\033[0m' + str(rotor_nw_rpm))
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  Angle = ' + '\033[0m' + str(rotor_nw_angle))
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Rotor NE')
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  RPM = ' + '\033[0m' + str(rotor_ne_rpm))
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  Angle = ' + '\033[0m' + str(rotor_ne_angle))
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Rotor SW')
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  RPM = ' + '\033[0m' + str(rotor_sw_rpm))
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  Angle = ' + '\033[0m' + str(rotor_sw_angle))
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Rotor SE')
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  RPM = ' + '\033[0m' + str(rotor_se_rpm))
                    print('\033[38;2;{r};{g};{b}m'.format(r=224, g=255, b=224) + '  Angle = ' + '\033[0m' + str(rotor_se_angle))
                else:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=0) + 'FAILURE = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=128, b=128) + "Rotors' States" + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=255, g=192, b=192) + ' Status Code = ' + '\033[0m' + str(response.status_code))
        except Exception as e:
            with print_lock:
                print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=0) + 'ERROR = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=128) + "Rotors' States" + '\033[0m')
                print('\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=192) + ' Exception = ' + '\033[0m' + str(e))

        time.sleep(interval)
# Coordinates
def send_coordinates():
    global last_coordinates
    interval = 1

    url = 'http://127.0.0.1:5000/send-coordinates'

    while True:
        try:
            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)

            coordinates = {'latitude': latitude, 'longitude': longitude}
            last_coordinates = coordinates

            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=coordinates, headers=headers)

            with print_lock:
                if response.status_code == 200:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'SUCCESS = ' + '\033[38;2;{r};{g};{b}m'.format(r=128, g=255, b=128) + 'Coordinates' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Latitude = ' + '\033[0m' + str(latitude))
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Longitude = ' + '\033[0m' + str(longitude))
                else:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=0) + 'FAILURE = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=128, b=128) + 'Coordinates' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=255, g=192, b=192) + ' Status Code = ' + '\033[0m' + str(response.status_code))
        except Exception as e:
            with print_lock:
                print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=0) + 'ERROR = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=128) + 'Coordinates' + '\033[0m')
                print('\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=192) + ' Exception = ' + '\033[0m' + str(e))

        time.sleep(interval)
# Mine Detection
def send_mine_detection():
    global mine_detected
    interval = 1

    url = 'http://127.0.0.1:5000/send-mine-detection'

    while True:
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json={'mine_detected': mine_detected}, headers=headers)

            with print_lock:
                if response.status_code == 200:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'SUCCESS = ' + '\033[38;2;{r};{g};{b}m'.format(r=128, g=255, b=128) + 'Mine Detection' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Value = ' + '\033[0m' + str(mine_detected))
                else:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=0) + 'FAILURE = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=128, b=128) + 'Mine Detection' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=255, g=192, b=192) + ' Status Code = ' + '\033[0m' + str(response.status_code))
        except Exception as e:
            with print_lock:
                print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=0) + 'ERROR = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=128) + 'Mine Detection' + '\033[0m')
                print('\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=192) + ' Exception = ' + '\033[0m' + str(e))

        mine_detected = not mine_detected

        time.sleep(interval)
# Battery Level
def send_battery_level():
    global battery_level
    interval = 10

    url = 'http://127.0.0.1:5000/send-battery-level'

    while True:
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json={'battery_level': battery_level}, headers=headers)

            with print_lock:
                if response.status_code == 200:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'SUCCESS = ' + '\033[38;2;{r};{g};{b}m'.format(r=128, g=255, b=128) + 'Battery Level' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=192, g=255, b=192) + ' Value = ' + '\033[0m' + str(battery_level))
                else:
                    print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=0) + 'FAILURE = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=128, b=128) + 'Battery Level' + '\033[0m')
                    print('\033[38;2;{r};{g};{b}m'.format(r=255, g=192, b=192) + ' Status Code = ' + '\033[0m' + str(response.status_code))
        except Exception as e:
            with print_lock:
                print('\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=0) + 'ERROR = ' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=128) + 'Battery Level' + '\033[0m')
                print('\033[38;2;{r};{g};{b}m'.format(r=255, g=255, b=192) + ' Exception = ' + '\033[0m' + str(e))

        time.sleep(interval)



# RESOURCES
# Hello
class Hello(Resource):
    def get(self):
        return jsonify({'message': 'Server is running...'})
# Flight Time
class FlightTime(Resource):
    def get(self):
        global flight_time

        return jsonify({'flight_time': flight_time})
    def post(self):
        data = request.json
        flight_time = data.get('flight_time')

        return jsonify({'flight_time': flight_time})
# Rotors' States
class RotorsStates(Resource):
    def get(self):
        global rotors_states

        return jsonify({'rotors_states': rotors_states})
    def post(self):
        data = request.json
        rotor_nw_rpm = data.get('rotor_nw_rpm')
        rotor_nw_angle = data.get('rotor_nw_angle')
        rotor_ne_rpm = data.get('rotor_ne_rpm')
        rotor_ne_angle = data.get('rotor_ne_angle')
        rotor_sw_rpm = data.get('rotor_sw_rpm')
        rotor_sw_angle = data.get('rotor_sw_angle')
        rotor_se_rpm = data.get('rotor_se_rpm')
        rotor_se_angle = data.get('rotor_se_angle')
        
        return jsonify({
            'rotors_states': {
                'rotor_nw': {
                    'rotor_nw_rpm': rotor_nw_rpm,
                    'rotor_nw_angle': rotor_nw_angle
                },
                'rotor_ne': {
                    'rotor_ne_rpm': rotor_ne_rpm,
                    'rotor_ne_angle': rotor_ne_angle
                },
                'rotor_sw': {
                    'rotor_sw_rpm': rotor_sw_rpm,
                    'rotor_sw_angle': rotor_sw_angle
                },
                'rotor_se': {
                    'rotor_se_rpm': rotor_se_rpm,
                    'rotor_se_angle': rotor_se_angle
                }
            }
        })
# Coordinates
class Coordinates(Resource):
    def get(self):
        global last_coordinates

        return jsonify({'last_coordinates': last_coordinates})
    def post(self):
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        return jsonify({
            'coordinates': {
                'latitude': latitude,
                'longitude': longitude
            }
        })
# Mine Detection
class MineDetection(Resource):
    def get(self):
        global mine_detected

        return jsonify({'mine_detected': mine_detected})
    def post(self):
        data = request.json
        mine_detected = data.get('mine_detected')

        return jsonify({'mine_detected': mine_detected})
# Battery Level
class BatteryLevel(Resource):
    def get(self):
        global battery_level

        return jsonify({'battery_level': battery_level})
    def post(self):
        data = request.json
        battery_level = data.get('battery_level')

        return jsonify({'battery_level': battery_level})

# adding the resources
api.add_resource(Hello, '/', methods=['GET'])
api.add_resource(FlightTime, '/send-flight-time', methods=['GET', 'POST'])
api.add_resource(RotorsStates, '/send-rotors-states', methods=['GET', 'POST'])
api.add_resource(Coordinates, '/send-coordinates', methods=['GET', 'POST'])
api.add_resource(MineDetection, '/send-mine-detection', methods=['GET', 'POST'])
api.add_resource(BatteryLevel, '/send-battery-level', methods=['GET', 'POST'])



# MAIN
if __name__ == '__main__':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.CRITICAL)

    print('\n\n\n' + '\033[38;2;{r};{g};{b}m'.format(r=255, g=0, b=255) + 'MINE DETECTION DRONE SERVER' + '\033[0m')
    print('\033[38;2;{r};{g};{b}m'.format(r=0, g=255, b=0) + 'Server is running...' + '\033[0m')

    t1 = threading.Thread(target=send_flight_time)
    t1.start()
    t2 = threading.Thread(target=send_rotors_states)
    t2.start()
    t3 = threading.Thread(target=send_coordinates)
    t3.start()
    t4 = threading.Thread(target=send_mine_detection)
    t4.start()
    t5 = threading.Thread(target=send_battery_level)
    t5.start()

    app.run(debug=False)


