import pygame as pg

import projectile
import settings as st


class Weapon:
    def __init__(self):
        self.damage = 6
        self.ammo_speed = 1
        self.countdown_speed = 1 / st.FPS * 3
        self.countdown = 0

    def update(self):
        if self.countdown > 0:
            self.countdown -= self.countdown_speed
        else:
            self.countdown = 0

    def shoot(self):
        mouse_pos = pg.mouse.get_pos()
        speed = st.TILES_WH // 10
        x, y = (mouse_pos[0] - st.WIDTH // 2), (mouse_pos[1] - st.HEIGHT // 2)

        vx = x / abs(x ** 2 + y ** 2) ** 0.5 * speed
        vy = y / abs(x ** 2 + y ** 2) ** 0.5 * speed

        self.countdown = 1
        projectile.Projectile("linear", (st.WIDTH // 2, st.HEIGHT // 2), (vx, vy),
                              st.TILES_WH * 5, self.damage)
