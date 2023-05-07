import numpy as np
import pygame as pg

import projectile
import settings as st
from weapon import Weapon


class Player(pg.sprite.Sprite):
    players = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((st.TILES_WH // 1.5, st.TILES_WH // 1.5))
        self.color = np.array((5, 5, 5))
        self.image.fill(self.color)

        # treeImage = pg.image.load("images/therock.png")
        # treeImage = pg.transform.scale(treeImage, (st.TILES_WH // 1.5, st.TILES_WH // 1.5))
        # self.image.blit(treeImage, (0, 0))

        self.rect = self.image.get_rect()
        self.rect.center = st.WIDTH // 2, st.HEIGHT // 2

        # stats
        self.max_hp = 5
        self.hp = self.max_hp
        self.mana = 1
        self.strength = 1
        self.agility = 1
        self.vitality = 1
        self.attack_speed = st.TICK * 2

        self.running = 0, 0
        self.shoot_bool = False
        self.is_alive = True
        self.take_damage_countdown = 1
        self.make_damage_countdown = 1

        st.all_sprites.add(self)
        Player.players.append(self)

    def update(self):
        self.take_damage_countdown = max(self.take_damage_countdown - st.TICK * 5, 0)
        self.make_damage_countdown = max(self.make_damage_countdown - self.attack_speed, 0)

    def check_health(self):
        dh = max(self.hp / self.max_hp, 0.1)
        clr = np.array([(1-dh)*100, 0, 0])
        pg.draw.rect(self.image, clr+self.color, (0, 0, *self.rect.size), self.rect.width // 10)
        pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def take_damage(self, dmg):
        if self.take_damage_countdown:
            return

        self.hp = max(self.hp - dmg, 0)
        self.check_health()
        if self.hp == 0:
            self.is_alive = False

    def move(self, x, y):
        # preparations
        v = max(st.TILES_WH * 3 * st.TICK, 1)
        offset = st.TILES_WH // 10 // 1.5
        x, y = -x, -y

        # player's and board's pos
        left, top, right, bottom = *self.rect.topleft, *self.rect.bottomright
        b_left, b_top = st.positions[0]

        # positions and offset
        t_bt = (top - b_top) / st.TILES_WH
        b_bt = (bottom - b_top) / st.TILES_WH
        l_bl = (left - b_left) / st.TILES_WH
        r_bl = (right - b_left) / st.TILES_WH
        offset_tiles = offset / st.TILES_WH

        # hit wall? great, now go back, Monkey
        ox, oy = 0, 0
        if st.map_tiles[int(t_bt)][int(l_bl - offset_tiles)] == "02":
            ox += 1
        elif st.map_tiles[int(t_bt)][int(r_bl + offset_tiles)] == "02":
            ox -= 1
        elif st.map_tiles[int(b_bt)][int(l_bl - offset_tiles)] == "02":
            ox += 1
        elif st.map_tiles[int(b_bt)][int(r_bl + offset_tiles)] == "02":
            ox -= 1

        if st.map_tiles[int(t_bt - offset_tiles)][int(l_bl)] == "02":
            oy += 1
        elif st.map_tiles[int(b_bt + offset_tiles)][int(l_bl)] == "02":
            oy -= 1
        elif st.map_tiles[int(t_bt - offset_tiles)][int(r_bl)] == "02":
            oy += 1
        elif st.map_tiles[int(b_bt + offset_tiles)][int(r_bl)] == "02":
            oy -= 1

        # this is needed for not being pushed from wall
        # upd: now, it doesn't work with diagonal movement, because of square root of 2 divided by 2.
        # It's an irrational number. Also, maybe it's because of it being little bit smaller than my program can detect.
        rx, ry = (1 if x else 0), (1 if y else 0)
        # sum it all up
        st.positions += ((x - ox) * v * rx, (y - oy) * v * ry)

    def shoot(self):
        mouse_pos = pg.mouse.get_pos()
        speed = st.TILES_WH // 10
        x, y = (mouse_pos[0] - st.WIDTH // 2), (mouse_pos[1] - st.HEIGHT // 2)

        vx = x / abs(x ** 2 + y ** 2) ** 0.5 * speed
        vy = y / abs(x ** 2 + y ** 2) ** 0.5 * speed

        self.make_damage_countdown = 1
        projectile.Projectile("linear", (st.WIDTH // 2, st.HEIGHT // 2), (vx, vy),
                              st.TILES_WH * 5, self.strength)

