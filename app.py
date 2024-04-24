import random
import requests
import threading
import time
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS



app = Flask(__name__)
api = Api(app)
CORS(app, origins=['http://localhost:3000']) # URL of the UI



# icon
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')



last_coordinates = {} # global variable to store the last sent coordinates



# random coordinate generator
def send_coordinates():
    global last_coordinates
    url = 'http://127.0.0.1:5000/send-coordinates' # URL of the coordinates to be sent
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



# Hello
class Hello(Resource):
    def get(self):
        return jsonify({'message': 'Hello World!'})
# Hello 2
class Hello_2(Resource):
    def get(self):
        return jsonify({'message': 'Hello again, World!'})

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



api.add_resource(Hello, '/', methods=['GET'])
api.add_resource(Hello_2, '/hello-2', methods=['GET'])
api.add_resource(Coordinates, '/send-coordinates', methods=['GET', 'POST'])



if __name__ == '__main__':
    # thread for sending coordinates
    t = threading.Thread(target=send_coordinates)
    print('Sending coordinates...')
    t.start()

    # main thread
    app.run(debug=True)


