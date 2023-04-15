import A_star
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
        self.color = (250, 100, 100)
        self.rect = self.image.get_rect()
        pos = pos[0] + st.TILES_WH // 2, pos[1] + st.TILES_WH // 2
        self.rect.center = pos
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
        self.die_stop = None
        self.way = None
        self.last_way = None
        self.player_was_at = None

        Enemy.number_of_enemies += 1

    def update(self):
        self.time += st.TICK
        if not self.spawn_stop:
            effects.spawn_mob(self)
            self.rect.center = st.positions[self.i]
            return
        if self.die_stop is not None:
            if self.die_stop is False:
                effects.die_mob(self)
                self.rect.center = st.positions[self.i]
                return
            else:
                self.destroy()
                return

        self.get_stronger()

        # positions
        center = st.WIDTH // 2, st.HEIGHT // 2
        pos = self.rect.center
        x1, y1 = center[0] - pos[0], center[1] - pos[1]

        # this is detect-radius, and if enemy is in it, then move
        radius = st.TILES_WH * 20
        if x1 ** 2 + y1 ** 2 <= radius ** 2:
            self.new_move()

        # update the position
        self.rect.center = st.positions[self.i]

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

        self.color = self.color[0] - 40, self.color[1] - 20, self.color[2] - 20

        self.change_self_color(self.color)

    def change_self_color(self, color):
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def take_damage(self, dmg):
        if not self.spawn_stop or self.die_stop is not None:
            return
        self.hp -= dmg
        if self.hp <= 0:
            self.die_stop = False
            self.time = 0

    def destroy(self):
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

    def new_move(self):
        self_pos = st.pos_to_tiles_plus_check(st.positions[self.i])
        if self_pos is not None:
            player_at = st.pos_to_tiles((st.WIDTH // 2, st.HEIGHT // 2))
            if self.player_was_at is None or self.player_was_at != player_at:
                self.player_was_at = player_at
                self.way = A_star.a_star_algorithm(self_pos, player_at)
            else:
                self.way = self.way[1:]
        if not self.way:
            return
        if len(self.way) == 1:
            return
        v = max(st.TILES_WH // 30, 1)
        vx, vy = self.way[1][0] - self.way[0][0], self.way[1][1] - self.way[0][1]
        if abs(vx+vy) != 1:
            vx, vy = vx * 0.8, vy * 0.8
        vx, vy = vx * v, vy * v
        st.positions[self.i] += (vx, vy)


def spawn_enemies(positions, monster_hp):
    for x in positions:
        pos = st.positions[0][0] + x[0] * st.TILES_WH, st.positions[0][1] + x[1] * st.TILES_WH
        Enemy(pos, monster_hp)
