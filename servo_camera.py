# -*- coding: utf-8 -*-
from StringIO import StringIO
from PIL import Image
import pygame
import pygame.camera
from pygame.locals import *

import platform, time, io

global_cam = None
pi_cam = None

if platform.system() == 'Windows':
    from VideoCapture import Device
    global_cam = Device(0)
else:
    import picamera

def is_windows():
    return (platform.system() == 'Windows')

def init_camera():
    pygame.init()
    pygame.camera.init()

def init_pi_cam():
    if not is_windows():
        global pi_cam
        global pi_buffer
        pi_cam = picamera.PiCamera()
        pi_cam.resolution = (320, 240)
        pi_cam.framerate = 30
        #pi_cam.start_preview()
        time.sleep(2)

def get_cam():
    global global_cam

    if global_cam == None:
        if is_windows():
            global_cam = Device()
        else:
            init_camera()
            global_cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (320, 240))
            global_cam.start()

    return global_cam

def get_pi_cam():
    global pi_cam

    if pi_cam == None:
        init_pi_cam()
    return pi_cam

def capture(path="./cap.jpg"):
    cam = get_cam()
    img = cam.get_image()
    pygame.image.save(img, path)
    return open(path).read()

def capture_to_memory():
    cam = get_cam()
    data = StringIO()

    if is_windows():
        img = cam.getImage(timestamp=1)
        img.save(data, 'JPEG')
    else:
        img = cam.get_image()
        img_str = pygame.image.tostring(img, 'RGB')
        pil_img = Image.fromstring('RGB', (320, 240), img_str)
        pil_img.save(data, 'JPEG')

    return data.getvalue()

def pi_cam_capture():
    stream = io.BytesIO()
    pi_cam = get_pi_cam()
    #start = time.time()
    pi_cam.capture(stream, format='jpeg', use_video_port=True)
    #end = time.time()
    #print 'fps: %.2f' % (1 / (end-start))
    return stream.getvalue()

if __name__ == '__main__':
    capture()
