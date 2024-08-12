import sqlite3

conn = sqlite3.connect("hero_factory.db")

c = conn.cursor()

c.execute(
    """CREATE TABLE IF NOT EXISTS hero_factory (
    name TEXT,
    max_hp INTEGER,
    base_min_damage INTEGER,
    base_max_damage INTEGER,
    attack_speed INTEGER,
    base_hit_chance INTEGER,
    block_chance INTEGER,
    level INTEGER,
    xp INTEGER,
    xp_to_next_level INTEGER
)"""
)

# List of Hero Data
all_heroes = [
    ("Warrior", 125, 35, 60, 4, 80, 20, 1, 0, 100),
    ("Priestess", 75, 25, 45, 5, 70, 30, 1, 0, 100),
    ("Thief", 75, 20, 40, 6, 80, 40, 1, 0, 100),
]

c.executemany(
    "INSERT INTO hero_factory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", all_heroes
)

c.execute("SELECT * FROM hero_factory")
my_data = c.fetchall()

for i in my_data:
    print(i)

conn.commit()
conn.close()
