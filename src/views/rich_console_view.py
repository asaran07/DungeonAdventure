from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from src.views.console_view import ConsoleView
from src.characters import Player
from src.characters.monster import Monster
from typing import List


class RichConsoleView(ConsoleView):
    def __init__(self):
        super().__init__()
        self.console = Console()

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

    def display_room_details(self, room):
        room_panel = Panel(
            f"[bold cyan]{room.name}[/bold cyan]\n\n{room.get_description()}",
            title="Current Room",
            expand=False,
        )
        self.console.print(room_panel)

    def display_combat_status(self, player: Player, monsters: List[Monster]):
        layout = Layout()
        layout.split_column(Layout(name="header"), Layout(name="body"))
        layout["body"].split_row(Layout(name="player"), Layout(name="monsters"))

        # Header
        layout["header"].update(Panel("Combat Status", style="bold red"))

        # Player status
        player_table = Table(title="Player", show_header=False)
        player_table.add_column("Attribute", style="cyan")
        player_table.add_column("Value", style="magenta")
        player_table.add_row("Name", player.name)
        player_table.add_row("HP", f"{player.hero.current_hp}/{player.hero.max_hp}")
        layout["player"].update(player_table)

        # Monsters status
        monster_table = Table(title="Monsters")
        monster_table.add_column("Name", style="cyan")
        monster_table.add_column("HP", style="magenta")
        for monster in monsters:
            monster_table.add_row(
                monster.name, f"{monster.current_hp}/{monster.max_hp}"
            )
        layout["monsters"].update(monster_table)

        self.console.print(layout)

    def display_message(self, message):
        self.console.print(Text(message, style="bold green"))

    def display_available_actions(self, game_model):
        actions = [
            "[cyan]move[/cyan] - Move to another room",
            "[cyan]map[/cyan] - Display the dungeon map",
            "[cyan]inventory[/cyan] - Check your inventory",
            "[cyan]take[/cyan] - Pick up an item",
            "[cyan]drop[/cyan] - Drop an item",
        ]
        actions_panel = Panel(
            "\n".join(actions), title="Available Actions", expand=False
        )
        self.console.print(actions_panel)
