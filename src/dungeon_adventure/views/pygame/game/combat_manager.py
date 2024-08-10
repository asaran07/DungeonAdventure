from dungeon_adventure.controllers.combat_controller import CombatController
from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.enums.combat_state import CombatState


class CombatManager:
    def __init__(self, game_world, combat_screen):
        self.game_world = game_world
        self.combat_screen = combat_screen
        self.combat_controller = None  # Will be initialized when combat starts
        self.player = game_world.composite_player
        self.monsters = []

    def initiate_combat(self, monsters):
        self.monsters = monsters
        self.game_world.game_model.game_state = GameState.IN_COMBAT
        self.combat_controller = CombatController(
            self.game_world.game_model, self.combat_screen
        )
        self.combat_controller.initiate_combat()

    def handle_combat_input(self, event):
        action = self.combat_screen.get_combat_input(event)
        if action:
            self.process_combat_action(action)

    def process_combat_action(self, action):
        if action == "attack":
            self.combat_controller.player_attack()
        elif action == "use_item":
            self.combat_controller.use_item()
        elif action == "flee":
            self.combat_controller.attempt_flee()

    def update(self):
        if (
            self.combat_controller
            and self.combat_controller.combat_state == CombatState.MONSTER_TURN
        ):
            self.combat_controller.monster_turn()

    def draw(self, surface):
        self.combat_screen.draw(surface, self.player, self.monsters)

    def is_combat_over(self):
        return self.game_world.game_model.game_state != GameState.IN_COMBAT

    def end_combat(self):
        self.game_world.game_model.game_state = GameState.EXPLORING
        self.monsters = []
        self.combat_controller = None
