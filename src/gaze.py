import numpy as np
from numpy.linalg import norm
from typing import Tuple

class IvtFilter:
    def __init__(self, v_threshold=1):
        self.reset()
        self.v_threshold = v_threshold

    def reset(self):
        self.gaze_points = []
        self.prev_t = -1
        self.prev_x = -1
        self.prev_y = -1

    def execute(self, t: int, x: float, y: float) -> Tuple[float, float]:
        if self.prev_t >= 0:
            v = norm([x - self.prev_x, y - self.prev_y]) / (t - self.prev_t)
            print('t:', t - self.prev_t, 'v:', v)

            if v >= self.v_threshold:
                self.reset()
                return x, y

        self.gaze_points.append([x, y])
        if len(self.gaze_points) > 15:
            del self.gaze_points[0]
        self.prev_x = x
        self.prev_y = y
        self.prev_t = t

#         weights = [1 for _ in self.gaze_points]
#         if len(weights) > 5:
#           weights[-5:] = [2.] * 5

#         fixation = np.average(self.gaze_points, axis=0, weights=weights)
        fixation = np.mean(self.gaze_points, axis=0)

        return fixation[0], fixation[1]
