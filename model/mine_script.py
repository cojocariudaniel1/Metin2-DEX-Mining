import random
import time

import cv2
import keyboard
import numpy as np
import win32api
import win32con
from pytesseract import pytesseract, Output
import pytesseract

from PIL import ImageFilter, ImageEnhance

from model.pytesseract_model import ocr_core

from model.check_image import image
import win32gui, win32ui
from win32api import GetSystemMetrics

def crop_with_pil(area, img):
    img_crop = img.crop(area)
    return ocr_core(img_crop)


def get_image_mine_box(image):
    cropeed_image = image.crop((602, 307, 157 + 602, 206 + 307))
    return cropeed_image


def check_if_mining(image):
    text = crop_with_pil((644, 265, 644 + 77, 265 + 16), image)
    if "Mining" in text or "ing" in text or "inin" in text:
        return True
    else:
        return False


imgs_list = [
    np.array(cv2.imread("imgs/m1.png")),
    np.array(cv2.imread("imgs/m2.png")),
    np.array(cv2.imread("imgs/m3.png")),
    np.array(cv2.imread("imgs/m4.png")),
    np.array(cv2.imread("imgs/m5.png")),
    np.array(cv2.imread("imgs/m6.png")),
    np.array(cv2.imread("imgs/m7.png")),
    np.array(cv2.imread("imgs/m8.png")),
    np.array(cv2.imread("imgs/m9.png")),
    np.array(cv2.imread("imgs/m10.png")),
]


def match_image(img, tga):
    img_array = np.array(img)
    tga_array = np.array(tga)

    gray_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

    if gray_img is None:
        raise Exception("Image")
    template = cv2.cvtColor(tga_array, cv2.COLOR_RGB2GRAY)
    if template is None:
        raise Exception("Template")
    # perform template matching
    result = cv2.matchTemplate(gray_img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    treshold = 0.96
    yloc, xloc = np.where(result >= treshold)
    return (xloc, yloc)


def draw_rectangles(image, x_coords, y_coords, template_width, template_height):
    img_with_rectangles = np.array(image)

    cv2.rectangle(img_with_rectangles, (x_coords, y_coords), (x_coords + template_width, y_coords + template_height),
                  (0, 255, 0), 1)

    return img_with_rectangles


def math_image(image):
    d = []
    for index, img in enumerate(imgs_list):
        x, y = match_image(img, image)
        if len(x) == 0 and len(y) == 0:
            d.append(index)
    if d:
        return d[0]


pos_list = [
    (82, 24),  # img1
    (105, 44),  # img2
    (47, 56),  # img3
    (118, 81),  # img4
    (91, 101),  # img5
    (38, 100),  # img6
    (13, 124),  # img7
    (44, 156),  # img8
    (79, 167),  # img9
    (113, 141),  # img10
]


def click(x_axis, y_axis):
    win32api.SetCursorPos((x_axis, y_axis))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(round(random.uniform(0.15, 0.20)))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def right_click(x_axis, y_axis):
    win32api.SetCursorPos((x_axis, y_axis))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    time.sleep(round(random.uniform(0.15, 0.25)))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def stop_script():
    return keyboard.is_pressed('esc')  # Poți utiliza orice buton dorești aici


def draw_lines(self, x, y, length):
    """
    Desenează două linii începând de la coordonatele (x, y) cu lungimea specificată.
    
    Parametri:
    x (int): Coordonata X de pornire.
    y (int): Coordonata Y de pornire.
    length (int): Lungimea liniilor.
    """
    dc = win32gui.GetDC(0)
    dcObj = win32ui.CreateDCFromHandle(dc)
    
    # Set the starting point of the first line
    dcObj.MoveTo((x, y))

    # Draw the first line (horizontal)
    dcObj.LineTo((x + length, y))

    # Move to the starting point of the second line
    dcObj.MoveTo((x + length, y))

    # Draw the second line (vertical)
    dcObj.LineTo((x + length, y + length))

    win32gui.ReleaseDC(self.hwnd, dc)
