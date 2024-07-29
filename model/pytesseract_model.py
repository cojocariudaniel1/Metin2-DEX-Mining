import time

import cv2
import numpy
import numpy as np
from pytesseract import pytesseract, Output
import pytesseract

from PIL import ImageFilter, ImageEnhance

pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'


def _pytess_config(img):
    custom_config = r'--oem 3 --psm 6'
    pytesseract.image_to_string(img, config=custom_config)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


def ocr_core(image):
    roi = image.filter(ImageFilter.GaussianBlur(radius=0.3))
    enhancer = ImageEnhance.Contrast(roi)
    roi = enhancer.enhance(1.0)

    text = pytesseract.image_to_string(roi)
    return text
