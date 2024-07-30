# Core Components - Characters

## DungeonCharacter Class

Location: `src/characters/dungeon_character.py`

Base class for all characters in the game.

### Key Attributes

- `name`: str
- `max_hp`: int
- `current_hp`: int
- `base_min_damage`: int
- `base_max_damage`: int
- `attack_speed`: int
- `base_hit_chance`: int

### Important Methods

- `attempt_attack(target: DungeonCharacter) -> int`: Perform an attack on the target
- `take_damage(damage: int)`: Apply damage to the character
- `heal(amount: int)`: Restore hit points

## Hero Class

Location: `src/characters/hero.py`

Represents the player character, inherits from `DungeonCharacter`.

### Additional Attributes

- `block_chance`: int
- `level`: int
- `xp`: int
- `equipped_weapon`: Optional[Weapon]

### Important Methods Hero

- `equip_weapon(weapon: Weapon)`: Equip a weapon and apply its stat modifiers
- `gain_xp(xp: int)`: Gain experience points and level up if necessary
- `level_up()`: Increase level and update stats

## Monster Class

Location: `src/characters/monster.py`

Represents enemy characters, inherits from `DungeonCharacter`.

### Additional Attributes Monster

- `heal_chance`: int
- `min_heal`: int
- `max_heal`: int
- `xp_reward`: int
- `loot`: List[Item]

### Important Methods Monster

- `attempt_heal() -> int`: Try to heal based on heal chance
- `drop_loot() -> List[Item]`: Return the monster's loot when defeated
