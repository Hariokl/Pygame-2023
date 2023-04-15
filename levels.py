from random import random

import settings as st
import enemy
import draw_gui


# Call Level() when entering new level. Right after drawing the level.
class Level:
    level = None

    def __init__(self):
        self.level = 1
        self.wave = 1
        self.time = 0

        self.spawn_rate = 0.1
        self.max_number_of_monsters_per_wave = 1
        self.number_of_monsters_per_wave = 0
        self.number_of_killed = 0
        self.number_of_kills = 100
        self.monsters_standard_hp = 10
        self.monsters_hp = self.monsters_standard_hp
        self.amplifier = 1.01
        self.spawn_max_per_frame = 2
        self.spawn_per_frame = 0
        self.monsters_spawn_time = 1  # 10 * 0.99**x
        # y = 10 / ( x / 100 + 1) - func to measure time to spawn monster
        Level.level = self

    def update(self):
        # print(f"\r{self.number_of_monsters}", end="")
        self.time += st.TICK
        self.monsters_spawn_time -= st.TICK
        if self.monsters_spawn_time <= 0:
            if self.number_of_monsters_per_wave == self.max_number_of_monsters_per_wave and enemy.Enemy.number_of_enemies == 0:
                self.update_wave()
            self.monsters_hp = (self.monsters_standard_hp * self.level) * self.amplifier ** self.time
            [ms.update() for ms in MonsterSpawner.monsterSpawners]
            print(f"\r{self.number_of_monsters_per_wave}", end="")
            self.monsters_spawn_time = 4 / (self.time / 150 + 1)
            self.spawn_per_frame = 0

    def update_wave(self):
        self.wave += 1
        self.max_number_of_monsters_per_wave = 10 * self.wave
        self.number_of_monsters_per_wave = 0
        draw_gui.diff_bar_dict["wave_time"] = 3
        enemy.Enemy.number_of_killed = 0


class MonsterSpawner:
    monsterSpawners = []

    # TODO: need to change this method of updating because it's very slow
    def __init__(self, t_pos):
        self.t_pos = t_pos
        MonsterSpawner.monsterSpawners.append(self)

    def update(self):
        level = Level.level
        where = ((self.t_pos[0] - st.WIDTH // st.TILES_WH) ** 2 + (self.t_pos[1] - st.HEIGHT // st.TILES_WH) ** 2) / 10
        if level.number_of_monsters_per_wave < level.max_number_of_monsters_per_wave:
            if random() * where <= level.spawn_rate:
                enemy.spawn_enemies([self.t_pos], level.monsters_hp)
                level.number_of_monsters_per_wave += 1

