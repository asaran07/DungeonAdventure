import pygame

from dungeon_adventure.views.pygame.game.game_world import GameWorld


class DebugManager:
    def __init__(self):
        self.debug_mode = False
        self.fps = 0
        self.fps_update_time = 0

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")

    def update_fps(self, clock: pygame.time.Clock):
        current_time = pygame.time.get_ticks()
        if current_time - self.fps_update_time > 1000:
            self.fps = clock.get_fps()
            self.fps_update_time = current_time

    def draw_debug_info(self, surface, game_world: GameWorld):
        if not self.debug_mode:
            return

        font = pygame.font.Font(None, 15)
        y_offset = 10
        line_height = 20

        debug_info = [
            f"Debug Mode: ON",
            f"FPS: {self.fps:.2f}",
            f"Current Room: {game_world.current_room.room.name}",
            f"Room Type: {game_world.current_room.room.room_type}",
            f"Room Image: {game_world.current_room.image_path.split('/')[-1]}",
            "Open Doors:",
        ]

        # Add open doors information
        for (
            direction,
            connected_room,
        ) in game_world.current_room.room.connections.items():
            if connected_room:
                debug_info.append(f"  {direction.name}: {connected_room.name}")

        # Add player position
        player_pos = game_world.composite_player.rect.center
        debug_info.append(f"Player Position: {player_pos}")
        debug_info.append(f"Player Name: {game_world.composite_player.name}")
        debug_info.append(
            f"Player HP: {game_world.composite_player.hero.current_hp}/{game_world.composite_player.hero.max_hp}"
        )

        for i, info in enumerate(debug_info):
            debug_surface = font.render(info, True, (255, 255, 255))
            surface.blit(debug_surface, (10, y_offset + i * line_height))
