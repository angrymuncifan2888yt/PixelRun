class Window:
    def __init__(self, manager, id_):
        self.window_manager = manager
        self.id = id_

    def handle_pygame_event(self, event):
        pass

    def close(self):
        self.window_manager.close_current_window()

    def update(self, delta_time):
        pass

    def draw(self, screen):
        pass