import logging
from typing import List, Optional

from dungeon_adventure.enums.combat_state import CombatState
from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.views.pygame.combat.combat_screen import CombatScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld


class CombatManager:
    def __init__(self, game_world: GameWorld):
        self.enable_input_receiving = False
        self.logger = logging.getLogger("dungeon_adventure.combat")
        self.game_world = game_world
        self.view: Optional[CombatScreen] = None
        self.player = game_world.composite_player
        self.monsters: List[Monster] = []
        self.combat_state: CombatState = CombatState.WAITING
        self.turn_order: List[Hero | Monster] = []

    def set_combat_screen(self, combat_screen: CombatScreen):
        self.logger.info("Initializing combat screen")
        self.view = combat_screen

    def start_combat(self):
        self.logger.info("Starting combat")
        self.setup_combat()

    def setup_combat(self):
        self.logger.info("Setting up combat")
        self.monsters = self.game_world.current_room.room.monsters
        self.determine_turn_order()
        self.display_combat_info()

    def determine_turn_order(self):
        self.logger.info("Determining turn order")
        self.turn_order = [self.player.hero] + self.monsters
        self.turn_order.sort(key=lambda x: x.attack_speed, reverse=True)

    def display_combat_info(self):
        if self.view:
            self.view.set_message("Combat Started!", self.on_setup_message_complete)
            self.view.display_stat_bars(
                self.player, True, True, True, self.on_stat_bars_displayed
            )
            self.view.display_monster_stats(
                self.monsters, self.on_monster_stats_displayed
            )
        else:
            self.logger.warning("Combat screen not initialized")

    def on_setup_message_complete(self):
        self.logger.debug("Setup message display completed")

    def on_stat_bars_displayed(self):
        self.logger.debug("Player stat bars displayed")

    def on_monster_stats_displayed(self):
        self.logger.debug("Monster stats displayed")

    def update(self, dt: float):
        if self.view:
            self.view.update(dt)

    def draw(self, surface):
        if self.view:
            self.view.draw(surface)

    def process_events(self, event):
        if self.view:
            self.view.handle_event(event)
        else:
            self.logger.warning("Combat screen not initialized")

    def wait_for_user_input(self, event):
        pass
