import time

class GestureDetector:
    def __init__(self):
        self.history = []
        self.roll_start_time = None
        self.gesture_timeout = 2  # seconds

    def update_iris_position(self, iris_coord):
        """Track iris positions to detect gestures"""
        self.history.append(iris_coord)
        if len(self.history) > 30:
            self.history.pop(0)

    def detect_eye_roll_click(self):
        """Detect a full eye roll (left→up→right→down→center)"""

        if len(self.history) < 20:
            return False

        xs = [x for x, y in self.history]
        ys = [y for x, y in self.history]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Basic circular motion threshold check
        wide_enough = (max_x - min_x) > 40
        tall_enough = (max_y - min_y) > 20

        if wide_enough and tall_enough:
            now = time.time()
            if self.roll_start_time is None or (now - self.roll_start_time) > self.gesture_timeout:
                self.roll_start_time = now
                return True  # Detected eye roll

        return False

    def detect_scroll_gesture(self, prediction_label):
        """
        Returns 'up', 'down' or None based on prediction
        """
        if prediction_label == "up":
            return "scroll_up"
        elif prediction_label == "down":
            return "scroll_down"
        return None
