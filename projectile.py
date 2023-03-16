import pygame as pg
import settings as st

from math import sin, pi


class Projectile(pg.sprite.Sprite):
    def __init__(self, motion, pos, v: tuple, max_radius, damage):
        pg.sprite.Sprite.__init__(self)
        translater = {"linear": self.linear, "sinusoida": self.sinusoida}

        self.image = pg.Surface((st.TILES_WH // 5, st.TILES_WH // 5))
        self.image.fill((250, 205, 205))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.v = v
        self.x = 0
        self.max_radius = max_radius
        self.start_pos = pos
        self.movement = translater[motion]
        self.damage = damage

        self.i = st.available_i[0]
        st.available_i.remove(self.i)
        st.positions[self.i] = pos
        st.all_sprites.add(self)

    def update(self):
        self.movement()
        self.check_hitted()
        self.rect.center = st.positions[self.i]

    def check_hitted(self):
        # player's and board's pos
        left, top, right, bottom = *self.rect.topleft, *self.rect.bottomright
        b_left, b_top = st.positions[0]

        # positions
        t_bt = (top - b_top) / st.TILES_WH
        b_bt = (bottom - b_top) / st.TILES_WH
        l_bl = (left - b_left) / st.TILES_WH
        r_bl = (right - b_left) / st.TILES_WH

        # better than having 1 check point (center), right?
        if st.map_tiles[int(t_bt)][int(l_bl)] == "02":
            self.destroy()
        elif st.map_tiles[int(b_bt)][int(l_bl)] == "02":
            self.destroy()
        elif st.map_tiles[int(t_bt)][int(l_bl)] == "02":
            self.destroy()
        elif st.map_tiles[int(t_bt)][int(r_bl)] == "02":
            self.destroy()

        # look for collision with enemy, if there is then the enemy must be damaged >:D
        for enemy in st.enemies_rects:
            if self.rect.colliderect(enemy.rect):
                self.destroy()
                enemy.take_damage(self.damage)

    def destroy(self):
        # need to change this
        # It did not work without set(), but after 10 hours of procrastination it is. Why? THE HELL SHOULD I KNOW!?!?!??
        # Update: Okay, now it is NOT working again... wtf?
        st.available_i.append(self.i)
        st.available_i = sorted(list(set(st.available_i)))
        #
        st.positions[self.i] = st.positions[0]
        st.all_sprites.remove(self)
        self.kill()

    # just movement
    def linear(self):
        self.x += st.TILES_WH / 130
        xs = self.x
        ys = 0
        self.move(xs, ys)

    # not done yet, this is pretty difficult :(
    # Update: I did it! I now understand how to implement any function to movement, and it will work :D
    def sinusoida(self):
        self.x += st.TILES_WH / 130
        xs = self.x
        ys = 4 * sin(xs / 5)
        self.move(xs, ys)

    # This one is to flip the coordinate system around its origin (0; 0),
    # and using this func I can add any math function as movement.
    # I was not the first one to come up with the solution to rotate coordinate-system,
    # but I MYSELF tried to come up with solution using math. And I did!! Moreover, It's the right one!!
    # All it took for me is 2 lessons.
    def move(self, xs, ys):
        x = xs * self.v[0] - ys * self.v[1]
        y = ys * self.v[0] + xs * self.v[1]

        st.positions[self.i] = x + self.start_pos[0], y + self.start_pos[1]

