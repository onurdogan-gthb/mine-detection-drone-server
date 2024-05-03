# IMPORTS
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



last_coordinates = {} # global variable to store the last sent coordinates



# FUNCTIONS
# Start
def send_start():
    url = 'http://127.0.0.1:5000/send-start'
    headers = {'Content-Type': 'application/json'}

    start = True

    time.sleep(15) # wait for 15 seconds initially

    try:
        response = requests.post(url, json={'start': start}, headers=headers)

        if response.status_code == 200:
            print('Start sent successfully: ', start)
        else:
            print('Failed to send start. Status code: ', response.status_code)
    except Exception as e:
        print('Error sending start: ', e)
# Coordinates
def send_coordinates():
    global last_coordinates
    url = 'http://127.0.0.1:5000/send-coordinates'
    while True:
        try:
            # generate random coordinates
            latitude = round(random.uniform(-90, 90), 6)
            longitude = round(random.uniform(-180, 180), 6)

            coordinates = {'latitude': latitude, 'longitude': longitude}
            last_coordinates = coordinates

            headers = {'Content-Type': 'application/json'}

            response = requests.post(url, json=coordinates, headers=headers)

            if response.status_code == 200:
                print('Coordinates sent successfully: ', coordinates)
            else:
                print('Failed to send coordinates. Status code: ', response.status_code)
        except Exception as e:
            print('Error sending coordinates: ', e)

        time.sleep(1) # send coordinates every 1 second
# Scan
def send_scan():
    url = 'http://127.0.0.1:5000/send-boolean'
    headers = {'Content-Type': 'application/json'}

    scan = True

    while True:
        try:
            response = requests.post(url, json={'scan': scan}, headers=headers)

            if response.status_code == 200:
                print('Scan sent successfully: ', scan)
            else:
                print('Failed to send scan. Status code: ', response.status_code)
        except Exception as e:
            print('Error sending scan: ', e)

        scan = not scan # flip the boolean

        time.sleep(3) # send scan every 3 seconds



# RESOURCES
# Hello
class Hello(Resource):
    def get(self):
        return jsonify({'message': 'Server is running...'})
# Start
class Start(Resource):
    def post(self):
        data = request.json
        start = data.get('start')
        print('The drone is started: {}'.format(start))
        return jsonify({'start': start})
# Coordinates
class Coordinates(Resource):
    def get(self):
        global last_coordinates
        return jsonify({'message': 'GET request received', 'last_coordinates': last_coordinates})
    def post(self):
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        print('Received coordinates: Latitude: {}, Longitude: {}'.format(latitude, longitude))
        return jsonify({'coordinates': {'latitude': latitude, 'longitude': longitude}})
# Scan
class Scan(Resource):
    def post(self):
        data = request.json
        scan = data.get('scan')
        print('Received scan: {}'.format(scan))
        return jsonify({'scan': scan})

# adding the resources
api.add_resource(Hello, '/', methods=['GET'])
api.add_resource(Start, '/send-start', methods=['POST'])
api.add_resource(Coordinates, '/send-coordinates', methods=['GET', 'POST'])
api.add_resource(Scan, '/send-scan', methods=['POST'])



# MAIN
if __name__ == '__main__':
    # thread for sending start
    t1 = threading.Thread(target=send_start)
    t1.start()
    # thread for sending coordinates
    t2 = threading.Thread(target=send_coordinates)
    t2.start()
    # thread for sending scan
    t3 = threading.Thread(target=send_scan)
    t3.start()

    # main thread
    app.run(debug=True)


