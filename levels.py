from random import random

import settings as st
from enemy import Enemy, spawn_enemies


# Call Level() when entering new level. Right after drawing the level.
class Level:
    level = None

    def __init__(self):
        self.spawn_rate = 0.05  # for practical
        # self.spawn_rate = 1  # for tests
        self.level = 1
        self.time = 0

        self.max_number_of_monsters = 50
        self.number_of_monsters = 0
        self.number_of_kills = 100
        self.monsters_standard_hp = 10
        self.monsters_hp = self.monsters_standard_hp
        self.amplifier = 1.01
        self.monsters_spawn_time = 10  # 10 * 0.99**x
        # y = 10 / ( x / 100 + 1) - func to measure time to spawn monster
        Level.level = self

    def update(self):
        # print(f"\r{self.number_of_monsters}", end="")
        time_passed = st.get_time("level")
        self.time += time_passed
        self.monsters_spawn_time -= time_passed
        if self.monsters_spawn_time <= 0:
            self.monsters_hp = (self.monsters_standard_hp * self.level) * self.amplifier ** self.time
            self.spawn_rate = 1 - 0.985 ** self.time  # for practical
            # self.spawn_rate = 1  # for tests
            [ms.update() for ms in MonsterSpawner.monsterSpawners]
            self.monsters_spawn_time = 10 / (self.time / 150 + 1)


class MonsterSpawner:
    monsterSpawners = []

    # TODO: need to change this method of updating because it's very slow
    def __init__(self, t_pos):
        self.t_pos = t_pos
        MonsterSpawner.monsterSpawners.append(self)

    def update(self):
        level = Level.level
        # radius = 15 ** 2
        # print(((st.WIDTH // 2 - self.t_pos[0]*st.TILES_WH) // st.TILES_WH) ** 2 + \
        #         ((st.HEIGHT // 2 - self.t_pos[1]*st.TILES_WH) // st.TILES_WH) ** 2, radius)
        # if not (((st.WIDTH // 2 - self.t_pos[0]*st.TILES_WH) // st.TILES_WH) ** 2 + \
        #         ((st.HEIGHT // 2 - self.t_pos[1]*st.TILES_WH) // st.TILES_WH) ** 2 <= radius):
        #     return
        if level.number_of_monsters < level.max_number_of_monsters:
            if random() <= level.spawn_rate:
                spawn_enemies([self.t_pos], level.monsters_hp)
                level.number_of_monsters += 1
