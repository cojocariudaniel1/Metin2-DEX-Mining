import random
import sys
import time
from threading import Thread
import win32gui, win32ui
from win32api import GetSystemMetrics
import cv2
import numpy as np
import win32api
import win32con
import keyboard
from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import QRect, Qt, QPoint, QCoreApplication
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QLineEdit

from design.style1.CheckBox import CheckBox

from design.style1.QLabelXButton import QLabelXButton
from design.style1.QTButtonCustom import Button
from model.check_image import image
from model.mine_script import check_if_mining, get_image_mine_box, stop_script, \
    match_image, draw_rectangles, click, right_click
import pyautogui

RES = 1920, 1080
APP_RES = 450, 450


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_loop_thread_run = True
        self.mine_loop_thread_run = False
        self.mine_loop_thread = Thread(target=self.mine_loop)
        self.mine_loop_thread.daemon = True

        self.start_time = time.time()
        self.main_loop = Thread(target=self.main_loop)
        self.main_loop.daemon = True
        self.main_loop.start()

        # Basic Settings
        self.new_window = None
        self.setObjectName("mainWindow")
        self.setGeometry(QRect(int(RES[0] / 2 - APP_RES[0] / 2), 75, APP_RES[0], APP_RES[1]))
        self.setStyleSheet("#mainWindow {background-color:#e6fcff}")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.dragging = False
        self.offset = QPoint()
        background_image = QLabel(self)
        pixmap = QPixmap("imgs/background_main_window.jpg")  # Setează calea către imagine
        scaled_pixmap = pixmap.scaled(APP_RES[0], APP_RES[1])

        background_image.setPixmap(scaled_pixmap)
        background_image.setGeometry(0, 0, APP_RES[0], APP_RES[1])

        self.title = QLabel("DEBUG: ", self)
        self.title.setGeometry(QRect(int(APP_RES[0] / 2 - self.title.width() - 90), 160, 400, 100))
        self.title.setStyleSheet("color: white")
        self.title.setFont(QtGui.QFont("Helvetica", 18))

        self.timer_label = QLabel("Timer (min): ", self)
        self.timer_label.setGeometry(QRect(40, 230, 300, 100))
        self.timer_label.setStyleSheet("color: white")
        self.timer_label.setFont(QtGui.QFont("Helvetica", 18))

        self.input_time = QLineEdit(self)
        self.input_time.setGeometry(QRect(190, 260, 90, 35))
        self.input_time.setFont(QtGui.QFont("Helvetica", 18))
        self.input_time.clearFocus()
        self.input_time.setText("720")

        self.timp_ramas = QLabel("Timp ramas (min): ", self)
        self.timp_ramas.setGeometry(QRect(40, 260, 300, 100))
        self.timp_ramas.setStyleSheet("color: white")
        self.timp_ramas.setFont(QtGui.QFont("Helvetica", 18))

        self.info = QLabel("Press:  SHIFT   for pause, RES: 1366x768", self)
        self.info.setGeometry(QRect(40, 290, 370, 100))
        self.info.setStyleSheet("color: green")
        self.info.setFont(QtGui.QFont("Helvetica", 15))

        self.info2 = QLabel("Display scalling 100%", self)
        self.info2.setGeometry(QRect(40, 320, 350, 100))
        self.info2.setStyleSheet("color: green")
        self.info2.setFont(QtGui.QFont("Helvetica", 15))

        pixmap = QPixmap("imgs/x_ button.png")
        pixmap = pixmap.scaled(25, 25, Qt.KeepAspectRatio)
        self.x_button = QLabelXButton(parent=self)
        self.x_button.setGeometry(QRect(APP_RES[0] - 45, 15, 25, 25))
        self.x_button.setPixmap(pixmap)
        self.x_button.signal.connect(self.exit)

        self.buton = Button("Start", self.start_main_loop, self)
        self.buton.setGeometry(QRect(90, 50, 280, 50))
        self.buton.setObjectName("QButtonCustom")
        
        self.btn_show_lines = Button("Show lines", self.toggle_draw_lines, self)
        self.btn_show_lines.setGeometry(QRect(90, 115, 280, 50))

        self.last_pos = None

        self.pos_list = [
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

        self.imgs_list = [
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
        
        self.drawing_lines = False
        self.hwnd = win32gui.WindowFromPoint((0, 0))
        self.monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

    def start_main_loop(self):
        if self.main_loop_thread_run:
            self.mine_loop_thread_run = True
            self.buton.setText("WORKING")
            self.buton.using_default = self.buton.working_style
            self.title.setText("DEBUG: APP STARTING")
            print(f"Mine Loop: {self.mine_loop_thread_run}")
            print("Press START")

    def exit(self):
        print("EXIT")
        del self.main_loop
        QCoreApplication.quit()
        sys.exit()

    def main_loop(self):
        time.sleep(0.3)
        while True:
            while self.main_loop_thread_run:
                print("DEBUG - APP Main loop - Running")
                self.title.setText("DEBUG: APP RUNING")
                if not self.mine_loop_thread_run:
                    del self.mine_loop_thread
                    self.mine_loop_thread = Thread(target=self.mine_loop).start()
                time.sleep(round(random.uniform(1, 2), 1))
                elapsed_time = time.time() - self.start_time
                if elapsed_time >= int(self.input_time.text()) * 60:  # 1800 sec = 30 min
                    self.exit()
                else:
                    self.timp_ramas.setText(
                        "Timp ramas (min): " + str(round(round(int(self.input_time.text()) * 60 - elapsed_time) / 60)))

                time.sleep(1)
            time.sleep(1)

    def mine_loop(self):
        time.sleep(2)
        print("START MINE LOOP")
        while self.mine_loop_thread_run:
            print("DEBUG: Mine Loop - RUNNING")
            self.title.setText("DEBUG: MINE LOOP RUNNING")
            app_image = image()
            mining_bool = check_if_mining(app_image[2])
            croped_image = get_image_mine_box(app_image[2])
            pos = self.math_image(croped_image)
            if stop_script():
                break
            if self.pause_mine():
                self.mine_loop_thread_run = False
                self.buton.setText("START")
                self.buton.using_default = self.buton.default_style
                self.buton.setStyleSheet(self.buton.default_style)
                self.buton.update()
                print(f"Mine Loop: {self.mine_loop_thread_run}")
                self.title.setText("DEBUG: MINE LOOP PAUSED")
                break

            if mining_bool:
                for index, i in enumerate(self.pos_list):
                    if stop_script():
                        break
                    if self.pause_mine():
                        self.mine_loop_thread_run = False
                        self.buton.setText("START")
                        self.buton.using_default = self.buton.default_style
                        self.buton.setStyleSheet(self.buton.default_style)
                        self.buton.update()
                        print(f"Mine Loop: {self.mine_loop_thread_run}")
                        self.title.setText("DEBUG: MINE LOOP PAUSED")
                        print("Press START")
                        break
                    if index == pos:
                        time.sleep(0.1)
                        click_time = round(random.uniform(0.10, 0.15), 1)
                        click(i[0] + app_image[0] + 602 + 10, i[1] + 10 + app_image[1] + 307)
                        time.sleep(click_time)
                        self.move_cursor(app_image[0] + 602 + random.randint(0, 150), app_image[1] + 307 + random.randint(-18, 0))

                        time.sleep(0.3)
                        pyautogui.mouseUp()
                        print("CLICKDD")
                        break
            else:
                time.sleep(0.2)
                self.title.setText("DEBUG: CLICK ORE")
                right_click(app_image[0] + 680, app_image[1] + 360)
                time.sleep(0.3)
                click(app_image[0] + 680, app_image[1] + 360)
                time.sleep(0.4)

            time.sleep(0.15)
        self.title.setText("DEBUG: MINE LOOP NOT RUNNING")
        print("DEBUG - Mine Loop - Not running")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()
            self.dragging = True

    def mouseMoveEvent(self, event):
        if self.dragging:
            new_pos = event.globalPos() - self.offset
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def pause_mine(self):
        return keyboard.is_pressed('shift')  # Poți utiliza orice buton dorești aici

    def math_image(self, image):
        d = []
        for index, img in enumerate(self.imgs_list):
            x, y = match_image(img, image)
            if len(x) == 0 and len(y) == 0:
                d.append(index)
        if d:
            return d[0]
    def move_cursor(self, x_axis, y_axis):
        win32api.SetCursorPos((x_axis, y_axis))
        
    def toggle_draw_lines(self):
            if self.drawing_lines:
                self.drawing_lines = False
                self.btn_show_lines.setText("Show lines")
            else:
                self.drawing_lines = True
                self.btn_show_lines.setText("Stop lines")
                Thread(target=self.draw_lines_loop).start()

    def draw_lines_loop(self):
        app_image = image()
        app_x, app_y = app_image[0], app_image[1]
        while self.drawing_lines:
            click_pos_box = [app_x + 690, app_y + 330,  6, 6]
            self.draw_lines(click_pos_box[0], click_pos_box[1], click_pos_box[2], click_pos_box[3])
            mine_window_pos = [app_x + 533, app_y + 288, 303, 236]
            self.draw_lines(mine_window_pos[0], mine_window_pos[1], mine_window_pos[2], mine_window_pos[3])
            win32gui.InvalidateRect(self.hwnd, self.monitor, True)

    def draw_lines(self, x, y, length, height):
        dc = win32gui.GetDC(0)

        rc = (x, y, x + length, y + height)
        win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_TOP)
        
        # Adjust the rect for vertical line
        rc = (x, y, x + length, y + height)
        win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_LEFT)
        
        # rc = (x, y, x + length, y + height)
        # win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_RIGHT)
        
        # rc = (x, y, x + length, y + height)
        # win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_BOTTOM)
        
        win32gui.ReleaseDC(self.hwnd, dc)