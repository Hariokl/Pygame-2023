import settings as st
from random import random
import pygame as pg
import numpy as np


def init():
    global all_sprites, tiles_display, td_pos, twh, player, positions
    all_sprites = pg.sprite.Group()

    twh = st.TILES_WH // 2
    tiles_display = pg.Surface((twh * 100, twh * 100))

    td_pos = (0, 0)
    player = None

    positions = [[None for _ in range(100)] for _ in range(100)]


class Tiles(pg.sprite.Sprite):
    def __init__(self, pos, tile_type=0):
        global player
        pg.sprite.Sprite.__init__(self)

        if positions[int(pos[1] // twh)][int(pos[0] // twh)] is not None:
            positions[int(pos[1] // twh)][int(pos[0] // twh)].destroy()

        if tile_type == 3:
            if player is not None:
                p_pos = player.pos
                positions[p_pos[1]][p_pos[0]] = Tiles((p_pos[0] * twh, p_pos[1] * twh), 1)
            player = self

        translate = {0: [pg.Color((0, 0, 0)), pg.Color((0, 0, 0))],
                     1: [pg.Color((200, 250, 90)), pg.Color((150, 200, 90))],
                     2: [pg.Color((250, 200, 90)), pg.Color((200, 150, 90))],
                     3: [pg.Color((200, 250, 90)), pg.Color((150, 200, 90)), pg.Color((20, 20, 250))],
                     4: [pg.Color((200, 250, 90)), pg.Color((150, 200, 90)), pg.Color((250, 100, 100))]}
        twh_ = twh // 20

        self.image = pg.Surface((twh, twh))
        self.image.fill(translate[tile_type][0])
        pg.draw.rect(self.image, translate[tile_type][1], (twh_, twh_, twh - twh_ * 2, twh - twh_ * 2), 0)

        if tile_type in [3, 4]:
            posses = (twh - twh // 1.5) // 2
            pg.draw.rect(self.image, translate[tile_type][2], (posses, posses, twh - posses * 2, twh - posses * 2), 0)

        self.rect = self.image.get_rect()
        self.tile_type = tile_type
        self.rect.topleft = pos
        all_sprites.add(self)

        positions[int(pos[1] // twh)][int(pos[0] // twh)] = self

        self.pos = [int(pos[0] // twh)]+[int(pos[1] // twh)]

        if tile_type == 0:
            self.destroy()

    def destroy(self):
        global player
        if player == self:
            player = None
        positions[self.pos[1]][self.pos[0]] = None
        all_sprites.remove(self)
        self.kill()


class Create_Map:
    def __init__(self):
        self.spawn_tile = 1
        self.draw = False
        self.running = 0, 0
        self.running_game = True

        self.display = pg.display.set_mode((st.WIDTH, st.HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("Map Maker")

        self.run()

    def run(self):
        while self.running_game:
            check_events(self)

            tiles_display.fill((0, 0, 0))
            all_sprites.update()
            all_sprites.draw(tiles_display)

            self.update()

            pg.display.flip()
            self.clock.tick(st.FPS)

    def draw_tile(self, pos):
        pos = ((pos[0] - td_pos[0]) // twh * twh, (pos[1] - td_pos[1]) // twh * twh)
        Tiles(pos, self.spawn_tile)

    def update(self):
        global td_pos
        td_pos = td_pos[0] + self.running[0], td_pos[1] + self.running[1]
        td_pos = max(min(td_pos[0], 0), -(100 - 20)*twh), max(min(td_pos[1], 0), -(100 - 15)*twh)
        self.display.blit(tiles_display, td_pos)


def check_events(game):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game.running_game = False

        if event.type == pg.MOUSEBUTTONDOWN:
            game.draw = True

        if event.type == pg.MOUSEBUTTONUP:
            game.draw = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                game.spawn_tile = 0
            if event.key == pg.K_1:
                game.spawn_tile = 1
            if event.key == pg.K_2:
                game.spawn_tile = 2
            if event.key == pg.K_3:
                game.spawn_tile = 3
            if event.key == pg.K_4:
                game.spawn_tile = 4

            if event.key == pg.K_w:
                game.running = game.running[0], 2
            if event.key == pg.K_s:
                game.running = game.running[0], -2
            if event.key == pg.K_a:
                game.running = 2, game.running[1]
            if event.key == pg.K_d:
                game.running = -2, game.running[1]

        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                game.running = game.running[0], 0
            if event.key == pg.K_s:
                game.running = game.running[0], 0
            if event.key == pg.K_a:
                game.running = 0, game.running[1]
            if event.key == pg.K_d:
                game.running = 0, game.running[1]
    if game.draw:
        game.draw_tile(pg.mouse.get_pos())


def circle_map(radius):
    tiles_map = ""
    center = (radius*2+3)//2
    for y in range(radius*2+3):
        for x in range(radius*2+3):
            pos = (center - x)**2 + (center - y)**2
            if pos == 0:
                tiles_map += "3"
            elif pos <= radius**2:
                tiles_map += "1" if random() / pos * radius ** 2> 0.2 else "4"
                print(0.2*pos / radius ** 2)
            elif pos <= (radius+1)**2:
                tiles_map += "2"
            else:
                tiles_map += "0"
        tiles_map += "\n"
    return tiles_map


def save_map(func=circle_map, radius=10):
    with open("maps.txt", "a") as maps_file:
        map_name = input()
        maps_file.write(f"# {map_name}\n")
        maps_file.writelines(func(radius))
        maps_file.writelines("\n")


def map_convertor(*args):
    # here I find borders of map
    left, right, top, bottom = None, None, None, None
    for j, y in enumerate(positions):
        for i, x in enumerate(y):
            if x is None:
                continue
            if left is None or i < left:
                left = i
            elif right is None or i > right:
                right = i
            if top is None or j < top:
                top = j
            elif bottom is None or j > bottom:
                bottom = j

    # then I translate and store new map to tiles_map
    translate = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    tiles_map = ""
    for y in positions[top:bottom + 1]:
        line = ""
        for x in y[left:right + 1]:
            if x is None:
                line += "0"
                continue
            line += str(translate[x.tile_type])
        tiles_map += line + "\n"
    return tiles_map


if __name__ == "__main__":
    # st.init()
    # init()
    # Create_Map()
    save_map(radius=19)
