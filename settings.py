import pygame as pg
import numpy as np
from time import time


def init():
    global WIDTH, HEIGHT, TILES_WH, FPS, display, positions, all_sprites, max_i, available_i, enemies_rects, list_of_who, gui_display, TICK, font30, font60
    WIDTH = 640*1.5
    HEIGHT = WIDTH * 0.75
    TILES_WH = max(WIDTH, HEIGHT) // 10 // 1.2
    FPS = 60
    TICK = 1 / FPS

    # number of different objects on map at the same time
    n = 4 * 1000

    display = pg.display.set_mode((WIDTH, HEIGHT))
    gui_display = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA, 32)
    gui_display = gui_display.convert_alpha()
    positions = np.full((n, 2), (0., 0.))
    all_sprites = pg.sprite.Group()
    max_i = n
    available_i = [i for i in range(n)]
    enemies_rects = list()
    list_of_who = {"level": None}

    pg.font.init()
    font30 = pg.font.SysFont('Comic Sans MS', 30)
    font60 = pg.font.SysFont('Comic Sans MS', 60)


def map_settings(map_name):
    global map_tiles
    with open("maps.txt") as maps_file:
        # троичная системма счистления получилась :D
        translate = {"0": "00", "1": "01", "2": "02", "3": "10", "4": "11"}
        readlines = False
        map_tiles = list()

        for line in maps_file.readlines():
            line = line.replace("\n", "")
            if line[2:] != map_name and not readlines:
                continue
            readlines = True

            if line[2:] == map_name:
                continue

            if line == "" and readlines:
                break

            map_tiles.append([translate[x] for x in line])


def tiles_to_pos(tile):
    return positions[0][0] + tile[0] * TILES_WH, positions[0][1] + tile[1] * TILES_WH


def pos_to_tiles_plus_check(pos):
    pos2 = tiles_to_pos((int((pos[0] - positions[0][0]) // TILES_WH), int((pos[1] - positions[0][1]) // TILES_WH)))
    pos2 = pos2[0] + TILES_WH // 2, pos2[1] + TILES_WH // 2
    rad = TILES_WH // 30
    if not check_in_rad(pos, pos2, rad):
        return None
    return int((pos[0] - positions[0][0]) // TILES_WH), int((pos[1] - positions[0][1]) // TILES_WH)

def pos_to_tiles(pos):
    return int((pos[0] - positions[0][0]) // TILES_WH), int((pos[1] - positions[0][1]) // TILES_WH)


def check_in_rad(pos1, pos2, rad):
    return ((pos2[0] - pos1[0]) ** 2 + (pos2[1] - pos1[1]) ** 2) <= rad


# # need to change the list_of_who method
# def get_time(who):
#     mate = list_of_who[who]
#     list_of_who[who] = time()
#     if mate is None:
#         return 0
#     return list_of_who[who] - mate

