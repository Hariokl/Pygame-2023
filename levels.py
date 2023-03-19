from random import random

import settings as st
from enemy import Enemy, spawn_enemies


# Call Level() when entering new level. Right after drawing the level.
class Level:
    level = None

    def __init__(self):
        self.spawn_rate = 0.1
        self.level = 1
        self.time = 0
        self.monsters_standard_hp = 10
        self.monsters_hp = self.monsters_standard_hp
        self.amplifier = 1.01
        self.monsters_spawn_time = 10  # 10 * 0.99**x
        # y = 10 / ( x / 100 + 1) - func to measure time to spawn monster
        Level.level = self

    def update(self):
        time_passed = st.get_time("level")
        self.time += time_passed
        self.monsters_spawn_time -= time_passed
        if self.monsters_spawn_time <= 0:
            [ms.update() for ms in MonsterSpawner.monsterSpawners]
            self.monsters_hp = (self.monsters_standard_hp * self.level) * self.amplifier ** self.time
            self.spawn_rate = 1 - 0.98 ** self.time
            self.monsters_spawn_time = 10 / (self.time / 100 + 1)


class MonsterSpawner:
    monsterSpawners = []

    # TODO: need to change this method of updating
    def __init__(self, t_pos):
        self.t_pos = t_pos
        MonsterSpawner.monsterSpawners.append(self)

    def update(self):
        if Level.level.monsters_spawn_time <= 0:
            if random() <= Level.level.spawn_rate:
                spawn_enemies([self.t_pos], Level.level.monsters_hp)
