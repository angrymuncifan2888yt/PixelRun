class WindowManager:
    def __init__(self):
        self.windows = []
        self.current_window = None
    
    def add_window(self, window):
        self.windows.append(window)
    
    def set_window(self, id_):
        for window in self.windows:
            if window.id == id_:
                self.current_window = window
                return
            
    def close_current_window(self):
        if self.current_window:
            self.current_window = None

    def handle_pygame_event(self, event):
        if self.current_window:
            self.current_window.handle_pygame_event(event)

    def update_current_window(self, delta):
        if self.current_window:
            self.current_window.update(delta)

    def draw_current_window(self, screen):
        if self.current_window:
            self.current_window.draw(screen)