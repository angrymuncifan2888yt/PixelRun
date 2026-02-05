class Timer:
    def __init__(self, duration: float, repeat=False):
        self.duration = duration
        self.repeat = repeat
        self.time = 0.0
        self.finished = False

    def update(self, delta_time: float):
        if self.finished:
            return

        self.time += delta_time

        if self.time >= self.duration:
            self.finished = True
            if self.repeat:
                self.time %= self.duration
                self.finished = False

    def reset(self):
        self.time = 0.0
        self.finished = False

    def is_finished(self):
        return self.finished