class Timer:
    def __init__(self, duration: float):
        self.duration = max(0.0, duration)
        self.time = 0.0
        self.finished = False

    def update(self, delta_time: float):
        if self.finished:
            return

        self.time += delta_time
        if self.time >= self.duration:
            self.finished = True

    def reset(self):
        self.time = 0.0
        self.finished = False
