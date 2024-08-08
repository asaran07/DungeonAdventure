import sqlite3

# Create and connect to monster_factory.db
conn = sqlite3.connect('monster_factory_new.db')

# Create cursor
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS monster_factory_new (
    name TEXT,
    max_hp INTEGER,
    base_min_damage INTEGER,
    base_max_damage INTEGER,
    attack_speed INTEGER,
    base_hit_chance INTEGER,
    heal_chance INTEGER,
    min_heal INTEGER,
    max_heal INTEGER,
    xp_reward INTEGER
    )""")

# List of Monster Data
all_monsters = [
    ('Skeleton', 100, 30, 50, 3, 80, 30, 30, 50, 25),
    ('Gremlin', 70, 15, 30, 5, 80, 40, 20, 40, 20),
    ('Ogre', 175, 30, 60, 2, 60, 10, 30, 60, 50)
]

# add data to table
c.executemany("INSERT INTO monster_factory_new VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", all_monsters)

#Query from the table
c.execute("SELECT * FROM monster_factory_new")
my_data = c.fetchall()

for i in my_data:
    print(i)

# Saves changes we've made
conn.commit()
#closes connection
conn.close()