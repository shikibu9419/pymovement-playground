import pywinctl as pwc
from typing import Optional, Tuple

class WindowManager:
    def __init__(self):
        print('Initializing WindowManager...')
        self.windows = [[w, w.getClientFrame()] for w in pwc.getAllWindows()]

    def getLookedWindow(self, gaze_point_x: float, gaze_point_y: float) -> Optional[pwc.Window]:
        for (w, rect) in self.windows:
            if rect.left < gaze_point_x < rect.right and rect.top < gaze_point_y < rect.bottom:
                print('Looked at', w.title)
                return w

        return None
