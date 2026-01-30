import pygame
from data import const, Sprites, Skins, FontStorage
from scene import SceneMainMenu, SceneManager, SceneType, SceneGame, SceneSkins, SceneLevels


class PixelRun:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(const.WINDOW_SIZE)
        Sprites.init()
        Skins.init()
        FontStorage.init()
        pygame.display.set_caption(const.WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()
        self.scene_main_menu = SceneMainMenu(self.scene_manager)
        self.scene_game = SceneGame(self.scene_manager)
        self.scene_skins = SceneSkins(self.scene_manager)
        self.scene_levels = SceneLevels(self.scene_manager)

        self.scene_manager.add_scene(self.scene_main_menu)
        self.scene_manager.add_scene(self.scene_game)
        self.scene_manager.add_scene(self.scene_skins)
        self.scene_manager.add_scene(self.scene_levels)
        self.scene_manager.set_scene(SceneType.MAIN_MENU)
    
    def mainloop(self):
        while self.running:
            delta_time = self.clock.tick(const.TARGET_FPS) / 1000

            self.scene_manager.update_current_scene(delta_time)
            self.scene_manager.render_current_scene(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.scene_manager.handle_event_current_scene(event)

            pygame.display.update()


if __name__ == "__main__":
    pixelrun = PixelRun()
    pixelrun.mainloop()
    