import win32gui
from PIL import ImageGrab

toplist, winlist = [], []

import time


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


def crop_image_opencv(img, area):
    img_crop = img.crop(area)
    return img_crop


def image():
    win32gui.EnumWindows(enum_cb, toplist)

    window = [(hwnd, title) for hwnd, title in winlist if 'Origins2 Evolution' in title]

    window = window[0]

    hwnd = window[0]
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(0.1)
    bbox = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox)
    x = bbox[0]
    y = bbox[1]

    return x, y, img
