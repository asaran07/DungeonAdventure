from typing import Dict

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.game.dungeon_adventure import GameModel
from src.views.view import View


class RichConsoleView(View):

    def __init__(self):
        super().__init__()
        self.console = Console()

    def display_title_screen(self):
        content = "Welcome to Dungeon Adventure!"
        box = Panel(content, title="Dungeon Adventure", expand=False)
        self.console.print(box)

    def get_player_creation_input(self) -> Dict:
        name = Prompt.ask("What's your name?")
        self.console.print(f"Welcome to the game, [bold]{name}[/bold].")
        return {"name": name}

    def get_user_input(self, prompt: str) -> str:
        choice = Prompt.ask(prompt)
        return choice

    def display_player_status(self, game_model):
        player = game_model.player
        hero = player.hero

        hero_status = Table(title="Hero Status", show_header=False)
        hero_status.add_column("Attribute", style="cyan")
        hero_status.add_column("Value", style="magenta")

        hero_status.add_row("Name", hero.name)
        hero_status.add_row("HP", f"{hero.current_hp}/{hero.max_hp}")
        hero_status.add_row("Level", str(hero.level))
        hero_status.add_row("XP", f"{hero.xp}/{hero.xp_to_next_level}")

        self.console.print(Panel(hero_status, expand=False))

    def display_available_actions(self, game_model: GameModel):
        pass

    def display_message(self, message):
        pass
