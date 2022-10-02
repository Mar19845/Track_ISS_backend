from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
from debris import Debris
TEMPLATES_AUTO_RELOAD = True

deb = Debris(
    '1 25544U 98067A   22274.03874838  .00014927  00000+0  26492-3 0  9996',
    '2 25544  51.6445 172.1493 0002537 314.1559  14.3121 15.50438125361599'
             )
# Start app
app = Flask(__name__)
CORS(app)

endpoint = '/api/v1'

@app.route(endpoint + '/', methods=['GET'])
def home():
    return render_template('index.html')
    
    
@app.route(endpoint + '/get_last_position', methods=['GET'])
def get_last_position():
    if request.method == 'GET':
        x,y,z = deb.animate()
        s = {
            "name": "ISS",
            'x':float(x[-1]),
            'y':float(y[-1]),
            'z':float(z[-1]),
            'current_velocity': deb.velocity,
            'current_position': deb.position,
            'julian_date':deb.jd,
            'fr':deb.fr,
            'time': deb.now,
            }
        return jsonify(s), 200
    
@app.route(endpoint + '/get_list_of_last_positions', methods=['GET'])
def get_last_positions():
    if request.method == 'GET':
        x,y,z = deb.animate()
        s = {
            "name": "ISS",
            'x':list(x),
            'y':list(y),
            'z':list(z),
            }
        return jsonify(s), 200

@app.route(endpoint + '/metrics',methods=['GET'])
def metrics():
    f=open('test.txt','r')
    data = f.read()
    print('data =',data)
    response = make_response(data, 200)
    response.mimetype = "text/plain"
    return response
    
# Start app on http://localhost:5000/api/v1
if __name__ == '__main__':
    #app.run(host="localhost", port=5000,debug=True)
    app.run(host='0.0.0.0', port=5000,debug=True)