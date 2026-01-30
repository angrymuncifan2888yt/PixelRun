from .scene import Scene

class SceneManager:
    def __init__(self):
        self.scenes = []
        self.current_scene = None

    def add_scene(self, scene):
        self.scenes.append(scene)

    def get_scene(self, id):
        for scene in self.scenes:
            if scene.id == id:
                return scene

        return ValueError("Scene not found")

    def set_scene(self, id):
        self.current_scene = self.get_scene(id)

    def handle_event_current_scene(self, event):
        if isinstance(self.current_scene, Scene):
            self.current_scene.handle_pygame_event(event)

    def update_current_scene(self, delta, **kvargs):
        if isinstance(self.current_scene, Scene):
            self.current_scene.update(delta, **kvargs)

    def render_current_scene(self, screen):
        if isinstance(self.current_scene, Scene):
            self.current_scene.draw(screen)
