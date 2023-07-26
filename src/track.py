import math

import tobii_research as tr
from pynput.mouse import Button, Controller
from pymovements.events import ivt
from gaze import IvtFilter
from one_euro_filter import OneEuroFilter

eyetracker = tr.find_all_eyetrackers()[0]

width = 3840
height = 2160

mouse = Controller()

now = (math.nan, math.nan)
ivt = IvtFilter(1)

one_euro_x = OneEuroFilter(beta=5)
one_euro_y = OneEuroFilter(beta=5)

def gaze_data_callback(gaze_data):
    gaze_points = (gaze_data.left_eye.gaze_point.position_on_display_area, gaze_data.right_eye.gaze_point.position_on_display_area)
    timestamp = gaze_data.system_time_stamp / 10000000

    # mean of left and right eye
    gaze_point_x = (gaze_points[0][0] + gaze_points[1][0]) / 2
    gaze_point_y = (gaze_points[0][1] + gaze_points[1][1]) / 2

    if math.isnan(gaze_point_x) or math.isnan(gaze_point_y):
        return

    # one euro filter
    gaze_point_x = one_euro_x(timestamp, gaze_point_x)
    gaze_point_y = one_euro_y(timestamp, gaze_point_y)

    # IvT (fixation) filter
    global now
    now = ivt.execute(timestamp, gaze_point_x, gaze_point_y)
    mouse.position = (now[0] * width, now[1] * height)
    print(now)

eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

while True: pass
#     if not (math.isnan(now[0]) or math.isnan(now[1])):
#         mouse.position = (now[0] * width, now[1] * height)
#         print(now)
#         print(mouse.position)

print('end.')

eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

