import pygame
from data import *
from scene import SceneManager, SceneType
from main import SceneMainMenu
from game import SceneGame
from scene_skins import SceneSkins
from scene_levels import SceneLevels
from scene_editor_playtest import SceneEditorPlaytest
from editor import SceneEditor


def init_assets():
    Sprites.init()
    Skins.init()
    Fonts.init()
    Levels.init()
    SoundChannels.init()
    Sounds.init()
    PlayerData.init()

class PixelRun:
    def __init__(self):
        # Core
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode(const.WINDOW_SIZE)
        pygame.display.set_caption(const.WINDOW_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True

        init_assets()

        # Scenes
        self.scene_manager = SceneManager()
        self.scene_main_menu = SceneMainMenu(self.scene_manager)
        self.scene_game = SceneGame(self.scene_manager)
        self.scene_skins = SceneSkins(self.scene_manager)
        self.scene_levels = SceneLevels(self.scene_manager)
        self.scene_editor = SceneEditor(self.scene_manager)
        self.scene_editor_playtest = SceneEditorPlaytest(self.scene_manager)

        self.scene_manager.add_scene(self.scene_main_menu)
        self.scene_manager.add_scene(self.scene_game)
        self.scene_manager.add_scene(self.scene_skins)
        self.scene_manager.add_scene(self.scene_levels)
        self.scene_manager.add_scene(self.scene_editor)
        self.scene_manager.add_scene(self.scene_editor_playtest)
        self.scene_manager.set_scene(SceneType.MAIN_MENU)

        # Background music
        pygame.mixer.music.load("assets/sounds/background.mp3")
        pygame.mixer.music.set_volume(PlayerData.MUSIC_VOLUME)

    def mainloop(self):
        pygame.mixer.music.play(-1)

        while self.running:
            delta_time = self.clock.tick(PlayerData.TARGET_FPS) / 1000

            self.scene_manager.update_current_scene(delta_time, clock=self.clock)
            self.scene_manager.render_current_scene(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.scene_manager.handle_event_current_scene(event)

            pygame.display.update()


if __name__ == "__main__":
    pixelrun = PixelRun()
    pixelrun.mainloop()
    