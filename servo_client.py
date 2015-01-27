import servo_camera
import platform

if platform.system() != 'Windows':
    import pigpio

pi = None
servo = 18
pulsewidth = 1500

def is_pi():
    return (platform.system() != 'Windows')

def pulsewidth_to_deg(pw):
    return ((pw - 500.0) * 180.0) / 2000.0

def move_servo(p):
    global pi
    global servo

    if pi == None:
        pi = init_pigpio(servo)

    if p < 500:
        p = 500
    elif p > 2500:
        p = 2500

    if is_pi():
        global pi
        global servo
        pi.set_servo_pulsewidth(servo, p)

    d = pulsewidth_to_deg(p)

    return p, d

def init_pigpio(addr):
    global pi
    global pulsewidth
    global servo
    servo = addr

    if is_pi():
        pi = pigpio.pi()
        pi.set_mode(addr, pigpio.OUTPUT)
        pi.set_servo_pulsewidth(servo, pulsewidth)
        
    return pi
