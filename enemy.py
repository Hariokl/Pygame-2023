import settings as st
import pygame as pg


class Enemy(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((st.TILES_WH // 1.5, st.TILES_WH // 1.5))
        self.image.fill((250, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.i = st.available_i[0]
        st.available_i.remove(self.i)

        st.all_sprites.add(self)
        st.positions[self.i] = pos
        st.enemies_rects.append(self)

        self.hp = 30

    def update(self):
        # positions
        center = st.WIDTH // 2, st.HEIGHT // 2
        pos = self.rect.center
        x1, y1 = center[0] - pos[0], center[1] - pos[1]

        # x- and y-movement
        x, y = 0, 0

        # this is detect-radius, and if enemy is in it, then move
        radius = st.TILES_WH * 8
        if x1 ** 2 + y1 ** 2 <= radius ** 2:
            # here "5" is constant for false-detection (or however it's called)
            if abs(x1) > 5:
                x = 1 if x1 - 5 > 0 else -1
            if abs(y1) > 5:
                y = 1 if y1 - 5 > 0 else -1
            self.move(x, y)

        # update the position
        self.rect.topleft = st.positions[self.i]

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        # need to change this
        st.available_i.append(self.i)
        st.available_i = sorted(list(set(st.available_i)))
        #
        st.positions[self.i] = st.positions[0]
        st.all_sprites.remove(self)
        st.enemies_rects.remove(self)
        self.kill()

    def move(self, x, y):
        # preparations
        v = max(st.TILES_WH // 30, 1)
        offset = st.TILES_WH // 10

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

        st.positions[self.i] += ((x + ox) * v, (y + oy) * v)


def spawn_enemies(positions):
    for x in positions:
        pos = st.positions[0][0] + x[0] * st.TILES_WH, st.positions[0][1] + x[1] * st.TILES_WH
        Enemy(pos)

