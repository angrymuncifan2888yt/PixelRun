import pygame
from data.player_data import PlayerData

def draw_world_grid(world, camera, screen):
    if not PlayerData.DRAW_WORLD_GRID:
        return

    cell_size = world.cell_size

    cam_x = camera.position.x
    cam_y = camera.position.y

    screen_w, screen_h = screen.get_size()

    start_x = int(cam_x // cell_size) * cell_size
    start_y = int(cam_y // cell_size) * cell_size

    end_x = start_x + screen_w + cell_size
    end_y = start_y + screen_h + cell_size

    for x in range(int(start_x), int(end_x), cell_size):
        pygame.draw.line(
            screen,
            PlayerData.WORLD_GRID_COLOR,
            (x - cam_x, 0),
            (x - cam_x, screen_h)
        )

    for y in range(int(start_y), int(end_y), cell_size):
        pygame.draw.line(
            screen,
            PlayerData.WORLD_GRID_COLOR,
            (0, y - cam_y),
            (screen_w, y - cam_y)
        )