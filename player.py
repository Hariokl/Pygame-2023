import pygame as pg

import settings as st
from weapon import Weapon


class Player(pg.sprite.Sprite):
    players = []

    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((st.TILES_WH // 1.5, st.TILES_WH // 1.5))
        self.image.fill((20, 20, 250))
        self.rect = self.image.get_rect()
        self.rect.center = st.WIDTH // 2, st.HEIGHT // 2

        self.weapon = Weapon()

        self.running = 0, 0
        self.shoot_bool = False

        st.all_sprites.add(self)
        Player.players.append(self)

    def update(self):
        self.weapon.update()

    def move(self, x, y, with_speed=True):
        # for teleportation which I still haven't started doing :D
        if not with_speed:
            st.positions += (x, y)
            return
        # preparations
        v = max(st.TILES_WH * 3 // st.FPS, 1)
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
        self.weapon.shoot()

