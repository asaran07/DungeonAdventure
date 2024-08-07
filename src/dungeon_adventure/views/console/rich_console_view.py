from typing import List

from rich.box import HEAVY
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.models.characters.monster import Monster
from dungeon_adventure.models.player import Player
from dungeon_adventure.views.console.console_view import (
    ConsoleView, PlayerNotExistException,
    UnsupportedGameStateException,
)
from src import GameModel


class RichConsoleView(ConsoleView):
    def __init__(self):
        super().__init__()
        self.console = Console()
        self.color_scheme = {
            "title": "bold magenta",
            "prompt": "cyan",
            "player": "green",
            "monster": "red",
            "item": "yellow",
            "action": "blue",
            "error": "bold red",
            "success": "bold green",
        }

    def display_message(self, message):
        self.console.print(message)

    def display_title_screen(self):
        title = Panel.fit(
            "Welcome to Dungeon Adventure!",
            style=self.color_scheme["title"],
            border_style="bold white",
        )
        self.console.print(title)
        self.console.print("1. Start New Game", style=self.color_scheme["action"])
        self.console.print("2. Load Game", style=self.color_scheme["action"])
        self.console.print("3. Quit", style=self.color_scheme["action"])


    def get_user_input(self, prompt: str) -> str:
        return Prompt.ask(f"[{self.color_scheme['prompt']}]{prompt}[/]")

    def get_player_creation_input(self) -> dict:
        name = self.get_user_input("Enter your character's name")
        if not name:
            self.console.print(
                "Player name cannot be empty", style=self.color_scheme["error"]
            )
            return self.get_player_creation_input()
        return {"name": name}

    def display_combat_status(self, player: Player, monsters: List[Monster]):
        layout = Layout()
        layout.split_column(
            Layout(name="header"),
            Layout(name="body"),
        )
        layout["body"].split_row(
            Layout(name="player"),
            Layout(name="monsters"),
        )

        layout["header"].update(Panel("Combat Status", style="bold white"))
        layout["player"].update(self._create_player_panel(player))
        layout["monsters"].update(self._create_monsters_panel(monsters))

        self.console.print(layout)

    def _create_player_panel(self, player: Player):
        return Panel(
            f"{player.name}\nHP: {player.hero.current_hp}/{player.hero.max_hp}\nXP: {player.hero.xp}/{player.hero.xp_to_next_level}",
            title="Player",
            style=self.color_scheme["player"],
            border_style="green",
        )

    def _create_monsters_panel(self, monsters: List[Monster]):
        monster_table = Table(show_header=False, box=HEAVY)
        for i, monster in enumerate(monsters, 1):
            monster_table.add_row(
                f"{i}. {monster.name}",
                f"HP: {monster.current_hp}/{monster.max_hp}",
            )
        return Panel(
            monster_table,
            title="Monsters",
            style=self.color_scheme["monster"],
            border_style="red",
        )

    def display_xp_gained(self, xp_amount: int):
        self.console.print(
            f"\n[{self.color_scheme['success']}]You gained {xp_amount} XP![/]"
        )

    def get_combat_action(self) -> str:
        actions = [
            ("1", "Attack"),
            ("2", "Use Item"),
            ("3", "Flee"),
        ]
        action_table = Table(title="Combat Actions", show_header=False, box=HEAVY)
        for number, action in actions:
            action_table.add_row(f"[{self.color_scheme['action']}]{number}[/]", action)
        self.console.print(action_table)

        while True:
            choice = self.get_user_input("Choose an action (1-3)")
            if choice in ["1", "2", "3"]:
                return ["attack", "use_item", "flee"][int(choice) - 1]
            self.console.print(
                "Invalid choice. Please enter 1, 2, or 3.",
                style=self.color_scheme["error"],
            )

    def display_player_status(self, game_model: GameModel):
        player = game_model.player
        if player is None:
            raise PlayerNotExistException("Player does not exist in the game model")

        status_panel = Panel(
            f"Player: {player.name}\n"
            f"HP: {player.hero.current_hp}/{player.hero.max_hp}\n"
            f"XP: {player.hero.xp}/{player.hero.xp_to_next_level}",
            title="Player Status",
            style=self.color_scheme["player"],
            border_style="green",
            expand=False,
        )
        self.console.print(status_panel)

    def display_available_actions(self, game_model):
        if game_model.game_state == GameState.EXPLORING:
            actions = [
                "move",
                "map",
                "inventory",
                "take",
                "drop",
                "stats",
                "equip",
                "use",
            ]
            action_table = Table(
                title="Available Actions", show_header=False, box=HEAVY
            )
            for action in actions:
                action_table.add_row(f"[{self.color_scheme['action']}]{action}[/]")
            self.console.print(action_table)
        else:
            raise UnsupportedGameStateException(
                f"Cannot display actions for game state: {game_model.game_state}"
            )

    def get_combat_target(self, monsters):
        monster_table = Table(title="Choose a target", show_header=False, box=HEAVY)
        for i, monster in enumerate(monsters, 1):
            monster_table.add_row(
                f"[{self.color_scheme['monster']}]{i}. {monster.name}[/]"
            )
        self.console.print(monster_table)

        while True:
            choice = self.get_user_input("Enter the number of the target")
            if choice.isdigit() and 1 <= int(choice) <= len(monsters):
                return monsters[int(choice) - 1]
            self.console.print(
                "Invalid choice. Please enter a valid number.",
                style=self.color_scheme["error"],
            )

    def display_room_description(self, room):
        description = Panel(
            room.get_desc(),
            title=room.name,
            style="bold white",
            border_style="blue",
        )
        self.console.print(description)
