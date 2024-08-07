import sys

import pygame

from src.characters.py_player import PyPlayer
from src.dungeon.py_room import PyRoom


class Application:
    def __init__(self, width=480, height=270):
        pygame.init()
        self.debug_mode = False
        self.width = width
        self.height = height
        self.scale_factor = 3
        self.window_width = self.width * self.scale_factor
        self.window_height = self.height * self.scale_factor
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.background = pygame.image.load(
            "/Users/saran/DungeonAdventure/src/resources/default_background.png"
        )
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )
        self.game_surface = pygame.Surface((self.width, self.height))
        pygame.display.set_caption("Dungeon Adventure")

        self.rooms = pygame.sprite.Group()
        room = PyRoom("/Users/saran/DungeonAdventure/src/resources/basic_room.png")
        room.rect.center = (self.width // 2, self.height // 2)
        self.rooms.add(room)

        self.player = pygame.sprite.GroupSingle()
        self.player_sprite = PyPlayer()
        self.player_sprite.rect.center = room.rect.center
        self.player.add(self.player_sprite)

        self.clock = pygame.time.Clock()

    def update(self):
        dt = self.clock.tick(60)
        # Technically we don't need this but if the rooms have different things
        # happening or different floor boundaries then this would be a good idea.
        current_room = next(iter(self.rooms.sprites()))
        self.player_sprite.update(dt, current_room.floor_rect)

    def draw(self):
        self.game_surface.blit(self.background, (0, 0))
        self.rooms.draw(self.game_surface)
        self.player.draw(self.game_surface)

        if self.debug_mode:
            current_room = next(iter(self.rooms.sprites()))
            current_room.draw_floor_rect(self.game_surface)
            self.player_sprite.draw_hitbox(self.game_surface)
            self.player_sprite.draw_debug_info(self.game_surface)
            self.draw_debug_info()

        scaled_surface = pygame.transform.scale(
            self.game_surface, (self.window_width, self.window_height)
        )
        self.screen.blit(scaled_surface, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    self.debug_mode = not self.debug_mode
                    print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        return True

    def draw_debug_info(self):
        if self.debug_mode:
            font = pygame.font.Font(None, 20)
            debug_surface = font.render("Debug Mode ON", True, (255, 255, 255))
            self.game_surface.blit(debug_surface, (10, 10))

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = Application()
    app.run()
