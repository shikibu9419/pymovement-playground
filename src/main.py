import tobii_research as tr
import numpy as np
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key
import pyautogui

from gaze import IvtFilter

import math
from time import time, sleep

# offset = [1920, 1080 - 416 - 70]
# width = 1440
# height = 900
offset = [0, 0]
width = 1920
height = 1080

listening = True
sleeping = False
now = (math.nan, math.nan)

eyetracker = tr.find_all_eyetrackers()[0]

mouse = Controller()

# def mouse_move(to_pos):
#     from_pos = (mouse.position[0], mouse.position[1])
# 
#     dist_x = to_pos[0] - from_pos[0]
#     dist_y = to_pos[1] - from_pos[1]
#     n = abs(int(min(dist_x, dist_y, 1000)))
#     print(from_pos, '->', to_pos, f'({n})')
# 
#     for i in range(n):
#         mouse.position = (from_pos[0] + dist_x / n * i, from_pos[1] + dist_y / n * i)
#         sleep(0.0001)

def on_press(key):
    print('{0} pressed'.format(key))
    global sleeping, listening

    if key == Key.enter:
        if sleeping:
            sleeping = False
        else:
            mouse.press(Button.left)
    if key == Key.esc:
        if not sleeping:
            sleeping = True
        else:
            listening = False
            # stop listening
            return False

def on_release(key):
    print('{0} released'.format(key))
    if key == Key.enter:
        mouse.release(Button.left)

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

filter = IvtFilter(v_threshold=0.5)

def gaze_data_callback(gaze_data):
    gaze_points = (gaze_data.left_eye.gaze_point.position_on_display_area, gaze_data.right_eye.gaze_point.position_on_display_area)
    timestamp = gaze_data.system_time_stamp
#     print(f"gazed: {gaze_points}")

    gaze_point_x = (gaze_points[0][0] + gaze_points[1][0]) / 2
    gaze_point_y = (gaze_points[0][1] + gaze_points[1][1]) / 2
    if math.isnan(gaze_point_x) or math.isnan(gaze_point_y):
        return

    global now
    now = filter.execute(timestamp / 1000000, gaze_point_x, gaze_point_y)

eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

while listening:
    # s = time()
    if sleeping:
        continue
    if not (math.isnan(now[0]) or math.isnan(now[1])):
#         print(now[0] * width + offset[0], now[1] * height + offset[1])
        pyautogui.moveTo(now[0] * width + offset[0], now[1] * height + offset[1], duration=0.5)
#         mouse_move((now[0] * width + offset[0], now[1] * height + offset[1]))
        # mouse.position = (now[0] * width + offset[0], now[1] * height + offset[1])
        # print(mouse.position)
        # sleep(0.05)
    # print(time() - s)

print('end.')

eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
