from typing import Callable
from datetime import datetime as dt
import csv

import tobii_research as tr

class EyeTracker:
    def __init__(self):
        self.eyetracker = tr.find_all_eyetrackers()[0]

    def create_callback(self, func: Callable, record_csv: bool):
        csvname = str(dt.now()).replace(' ', 'T') + '.csv'

        if record_csv:
            with open(csvname, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['left_x', 'left_y', 'right_x', 'right_y'])

        def callback(gaze_data):
            if record_csv:
                with open(self.csvname, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                      gaze_data.left_eye.gaze_point.position_on_display_area[0],
                      gaze_data.left_eye.gaze_point.position_on_display_area[1],
                      gaze_data.right_eye.gaze_point.position_on_display_area[0],
                      gaze_data.right_eye.gaze_point.position_on_display_area[1],
                  ])

            func(gaze_data)

        return callback

    def subscribe(callback: Callable, record_csv=False):
        self.eyetracker_callback = create_callback(callback, record_csv)
        eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.eyetracker_callback)

    def unsubscribe():
        eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.eyetracker_callback)
