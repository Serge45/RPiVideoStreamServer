import pigpio
from flask import Flask, render_template, request
from flask import Response, jsonify
import servo_camera
app = Flask(__name__, static_folder="static")

pi = None
servo = 18
pulsewidth = 1500

@app.route("/")
def index():
    return render_template("index.html", 
                           slider_value=pulsewidth,
                           servo_deg=180)

@app.route("/", methods=['POST'])
def move_servo():

    if request.method == 'POST':
        p = int(request.form['slider'])

        if p < 500:
            p = 500
        elif p > 2500:
            p = 2500

        global pi
        global servo
        pi.set_servo_pulsewidth(servo, p)
        d = ((p - 500.0) * 360.0) / 2000.0

    return render_template("index.html", 
                           slider_value=p,
                           servo_deg=d)

@app.route("/_move_servo")
def move_servo_ajax():
    print 'Move servo'
    p = request.args.get("pulsewidth", 1500, type=int)

    if p < 500:
        p = 500
    elif p > 2500:
        p = 2500

    global pi
    global servo
    pi.set_servo_pulsewidth(servo, p)
    deg = ((p - 500.0) * 360.0) / 2000.0
    return jsonify(result=deg)

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


def init_pigpio(addr):
    global pi
    global pulsewidth
    global servo
    servo = addr
    pi = pigpio.pi()
    pi.set_mode(addr, pigpio.OUTPUT)
    pi.set_servo_pulsewidth(servo, pulsewidth)
    return pi
    

if __name__ == '__main__':
    global servo
    init_pigpio(servo)
    app.run(threaded=True, host='0.0.0.0', debug=True)
