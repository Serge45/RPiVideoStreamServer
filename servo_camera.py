# -*- coding: utf-8 -*-
from StringIO import StringIO
from PIL import Image
import pygame
import pygame.camera
from pygame.locals import *

global_cam = None

def init_camera():
    pygame.init()
    pygame.camera.init()

def get_cam():
    global global_cam

    if global_cam == None:
        init_camera()
        global_cam = pygame.camera.Camera(pygame.camera.list_cameras()[0], (320, 240))
        global_cam.start()
    return global_cam

def capture(path="./cap.jpg"):
    cam = get_cam()
    img = cam.get_image()
    pygame.image.save(img, path)
    return open(path).read()

def capture_to_memory():
    cam = get_cam()
    img = cam.get_image()
    img_str = pygame.image.tostring(img, 'RGB')
    pil_img = Image.fromstring('RGB', (320, 240), img_str)
    data = StringIO()
    pil_img.save(data, 'JPEG')
    return data.getvalue()

if __name__ == '__main__':
    capture()
