# python -m venv .venv
import numpy as np
import cv2 # pip install opencv-python
from mss import mss # pip install mss

def color_compare(color1, color2):
    if np.sum(color1) <= np.sum(color2): return True
    else: return False

def image_transform(img_input):
        img_input = cv2.cvtColor(img_input, cv2.COLOR_RGB2GRAY)
        img_input = cv2.GaussianBlur(img_input, (9, 9), 0)
        img_input = cv2.Canny(img_input, 150, 160)
        return img_input

def contours_search(img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        con = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        return con

def work_img_create(img, con):
        for cont in con:
                sm = cv2.arcLength(cont, True)
                apd = cv2.approxPolyDP(cont, 0.0001*sm, True)
                cv2.drawContours(img, [apd], -1, (254, 19, 186), 4)
        return img

bounding_box = {'top': 0, 'left': 0, 'width': int(1280 * 0.7) , 'height': 1440}
# bounding_box = {'top': 200, 'left': 0, 'width': 400, 'height': 400}

sct = mss()

img = np.array(sct.grab(bounding_box))
while True:
    img_new = np.array(sct.grab(bounding_box))
    img_new_ = image_transform(img_new)
    con = contours_search(img_new_)
    cv2.imshow('screen', work_img_create(img, con))

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
            img = np.array(sct.grab(bounding_box))

    if (cv2.waitKey(1) & 0xFF) == ord(']'):
        cv2.destroyAllWindows()
        break