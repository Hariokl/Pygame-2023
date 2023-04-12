import effects
import settings as st
import pygame as pg


class Enemy(pg.sprite.Sprite):
    number_of_enemies = 0
    number_of_killed = 0

    def __init__(self, pos, hp):
        # import map
        # global map
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((st.TILES_WH // 1.5, st.TILES_WH // 1.5), pg.SRCALPHA, 32).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.mask = pg.mask.from_surface(self.image)

        self.time_county = 0  # delete this after optimizations
        self.last_vxy = 0, 0
        self.time = 0

        self.i = st.available_i[0]
        st.available_i.remove(self.i)

        st.all_sprites.add(self)
        st.positions[self.i] = pos
        st.enemies_rects.append(self)

        self.level = 1
        self.max_level = 5
        self.exp = 100
        self.hp = hp
        self.max_hp = hp

        self.spawn_stop = False

        Enemy.number_of_enemies += 1

    def update(self):
        self.time += st.TICK
        if not self.spawn_stop:
            effects.spawn_mob(self)
            self.rect.topleft = st.positions[self.i]
            return

        self.get_stronger()

        # positions
        center = st.WIDTH // 2, st.HEIGHT // 2
        pos = self.rect.center
        x1, y1 = center[0] - pos[0], center[1] - pos[1]

        # x- and y-movement
        x, y = 0, 0

        # this is detect-radius, and if enemy is in it, then move
        radius = st.TILES_WH * 20
        if x1 ** 2 + y1 ** 2 <= radius ** 2:
            # here "5" is constant for false-detection (or however it's called)
            if abs(x1) > 5:
                x = 1 if x1 - 5 > 0 else -1
            if abs(y1) > 5:
                y = 1 if y1 - 5 > 0 else -1
            self.move(x, y)

        # update the position
        self.rect.topleft = st.positions[self.i]

    def get_stronger(self):
        if self.level == self.max_level:
            return
        exp = self.time * 10
        if self.exp <= exp:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.hp *= 1.25
        self.max_hp *= 1.25
        self.exp = self.level * 100
        self.time = 0

        self.change_self_color((255 - (self.level - 1) * 40, 100 - (self.level - 1) * 20, 100 - (self.level - 1) * 20))

    def change_self_color(self, color):
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def take_damage(self, dmg):
        if not self.spawn_stop:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.destroy()

    def destroy(self):
        from levels import Level
        # need to change this
        st.available_i.append(self.i)
        st.available_i = sorted(list(set(st.available_i)))
        #
        st.positions[self.i] = st.positions[0]
        st.all_sprites.remove(self)
        st.enemies_rects.remove(self)
        Enemy.number_of_enemies -= 1
        Enemy.number_of_killed += 1
        self.kill()

    # Used to be with Borders
    # def new_move(self, x, y):
    #     for i, border in enumerate([map.Borders.b_borders, map.Borders.t_borders, map.Borders.r_borders, map.Borders.l_borders]):
    #         if pg.sprite.collide_mask(self, border):
    #             x += x ** 2 * (1 if i == 3 else (-1 if i == 2 else 0))
    #             y += y ** 2 * (1 if i == 1 else (-1 if i == 0 else 0))
    #     v = max(st.TILES_WH // 30, 1)
    #     st.positions[self.i] += x * v, y * v

    def move(self, x, y):
        # preparations
        v = max(st.TILES_WH // 30, 1)
        offset = st.TILES_WH // 10

        if self.time_county <= 3:
            st.positions[self.i] += self.last_vxy[0]*v, self.last_vxy[1]*v
            self.time_county += 1
            return
        self.time_county -= 3

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
        self.last_vxy = ((x + ox), (y + oy))


def spawn_enemies(positions, monster_hp):
    for x in positions:
        pos = st.positions[0][0] + x[0] * st.TILES_WH, st.positions[0][1] + x[1] * st.TILES_WH
        Enemy(pos, monster_hp)
