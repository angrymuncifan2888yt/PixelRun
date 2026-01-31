import pygame

class Entity:
    def __init__(self, world, position: pygame.Vector2, width, height, rotation=0):
        self.world = world
        self.position = position
        self.width = width
        self.height = height
        self.rotation = rotation
        self.hitbox = pygame.rect.Rect((self.position.x, self.position.y), (self.width, self.height))
        self.invisible = False

    def emit_event(self, event):
        self.world.event_bus.emit(event)

    def update_hitbox(self):
        self.hitbox.x = int(self.position.x)
        self.hitbox.y = int(self.position.y)
        self.hitbox.width = self.width
        self.hitbox.height = self.height

    def on_entity_collision(self, entity):
        pass

    def update(self, delta_time: float):
        pass
    
    def destroy(self):
        self.world.remove_entity(self)
