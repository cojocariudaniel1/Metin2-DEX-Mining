import time
import win32gui, win32ui
from win32api import GetSystemMetrics
import win32con
import win32api
# Initialize the device context and other variables
dc = win32gui.GetDC(0)
dcObj = win32ui.CreateDCFromHandle(dc)
hwnd = win32gui.WindowFromPoint((0, 0))
monitor = (0, 0, GetSystemMetrics(0), GetSystemMetrics(1))

def draw_lines(x, y, length, height):
    """
    Desenează două linii începând de la coordonatele (x, y) cu lungimea specificată.
    
    Parametri:
    x (int): Coordonata X de pornire.
    y (int): Coordonata Y de pornire.
    length (int): Lungimea liniilor.
    """
    red_pen = win32ui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 0, 0))
  
    dc = win32gui.GetDC(0)

    rc = (x, y, x + length, y + height)
    win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_TOP)
    
    # Adjust the rect for vertical line
    rc = (x, y, x + length, y + height)
    win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_LEFT)
    
    rc = (x, y, x + length, y + height)
    win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_RIGHT)
    
    rc = (x, y, x + length, y + height)
    win32gui.DrawEdge(dc, rc, win32con.EDGE_RAISED, win32con.BF_BOTTOM)
    
    win32gui.ReleaseDC(hwnd, dc)

while True:
    draw_lines(555, 333, 400, 100)
    win32gui.InvalidateRect(hwnd, monitor, True)

