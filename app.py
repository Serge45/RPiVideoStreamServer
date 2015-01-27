# -*-coding: utf-8 -*-
from flask import Flask, render_template, request
from flask import Response, jsonify
import servo_camera
import servo_client

import sys
import os.path

app = Flask(__name__, static_folder="static")

def install_secret_key(app, filename='secret_key'):
    filename = os.path.join(app.instance_path, filename)

    try:
        app.config['SECRET_KEY'] = open(filename, 'rb').read()
    except IOError:
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))

        f = open(filename, 'wb')
        f.write(os.urandom(24))
        f.close()
        sys.exit(1)


@app.route("/")
def index():
    return render_template("index.html", 
                           slider_value=1500,
                           servo_deg=180)

@app.route("/", methods=['POST'])
def move_servo():
    print 'POST: Move servo'

    if request.method == 'POST':
        p = int(request.form['slider'])

        ret_values = servo_client.move_servo(p)

    return render_template("index.html", 
                           slider_value=ret_values[0],
                           servo_deg=ret_values[1])

@app.route("/_move_servo")
def move_servo_ajax():
    print 'Ajax: Move servo'
    p = request.args.get("pulsewidth", 1500, type=int)

    ret_values = servo_client.move_servo(p)

    return jsonify(result=ret_values[1])

def get_camera_frame():
    while True:
        #frame = servo_camera.capture('./static/cap.jpg')
        frame = servo_camera.capture_to_memory()
        yield (b'--frame\r\n' +
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(get_camera_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    install_secret_key(app)
    app.run(threaded=True, host='0.0.0.0', debug=True)
