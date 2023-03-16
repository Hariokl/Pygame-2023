import pygame as pg
import numpy as np


def init():
    global WIDTH, HEIGHT, TILES_WH, FPS, display, positions, all_sprites, max_i, available_i, enemies_rects
    WIDTH, HEIGHT = 640*1.5, 480*1.5
    TILES_WH = max(WIDTH, HEIGHT) // 10 // 1.2
    FPS = 60

    # number of different objects on map at the same time
    n = 100

    display = pg.display.set_mode((WIDTH, HEIGHT))
    positions = np.full((n, 2), (0., 0.))
    all_sprites = pg.sprite.Group()
    max_i = n
    available_i = [i for i in range(n)]
    enemies_rects = list()


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
