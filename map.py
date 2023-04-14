import settings as st
from levels import MonsterSpawner
import pygame as pg
import A_star


class Map(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        st.map_settings("circle_15")

        self.map_tiles = st.map_tiles
        self.i = st.available_i[0]
        st.available_i.remove(self.i)

        tmap, player_pos = draw_map(self.map_tiles)

        self.image = tmap
        self.rect = self.image.get_rect()

        st.all_sprites.add(self)
        st.positions -= player_pos

    def update(self):
        self.rect.topleft = st.positions[self.i]


def draw_map(tmap):
    map = pg.Surface((len(tmap[0])*st.TILES_WH, len(tmap)*st.TILES_WH))
    twh = st.TILES_WH // 20
    grid = [[0] * len(tmap[0]) for _ in range(len(tmap))]
    # borders = Borders(map.get_size())
    for j, y in enumerate(tmap):
        for i, x in enumerate(y):
            if x == "00":
                continue
            color, color1 = get_color(x)
            grid[j][i] = 1
            if x == "02":
                grid[j][i] = 1000  # here the bigger this value the fewer errors may occur
            if x == "11":
                MonsterSpawner((i, j))
            if x == "10":
                player_pos = i*st.TILES_WH - st.WIDTH // 2 + st.TILES_WH // 2, \
                             j*st.TILES_WH - st.HEIGHT // 2 + st.TILES_WH // 2
            pg.draw.rect(map, color, (i*st.TILES_WH, j*st.TILES_WH, st.TILES_WH, st.TILES_WH), 0)
            pg.draw.rect(map, color1, (i*st.TILES_WH+twh, j*st.TILES_WH+twh, st.TILES_WH-twh*2, st.TILES_WH-twh*2), 0)

    # borders.configuration()
    A_star.setup(grid)
    return map, player_pos


# return colors based on type of tile
def get_color(xx):
    if xx in ["10", "11", "01"]:
        return pg.Color((200, 250, 90)), pg.Color((150, 200, 90))
    if xx == "00":
        return pg.Color((0, 0, 0)), pg.Color((0, 0, 0))
    if xx == "02":
        return pg.Color((250, 200, 90)), pg.Color((200, 150, 90))
