class Timer:
    def __init__(self, duration: float, repeat=False):
        self.duration = max(0.0, duration)
        self.repeat = repeat
        self.time = 0.0
        self.finished = False

        if self.duration == 0:
            self.finished = True

    def update(self, delta_time: float):
        if self.duration == 0:
            self.finished = True
            return

        if self.finished:
            return

        self.time += delta_time

        if self.time >= self.duration:
            if self.repeat:
                self.time %= self.duration
            else:
                self.finished = True

    def reset(self):
        self.time = 0.0
        self.finished = self.duration == 0

    def is_finished(self):
        return self.finished
