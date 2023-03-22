import pygame as pg
import settings as st
from levels import Level


def setup():
    global diff_bar_dict
    diff_bar_dict = {"width": st.WIDTH * 2 // 7, "height": st.HEIGHT / 12, "pos": (st.WIDTH * 2 // 3, st.HEIGHT // 15)}


def update():
    scr = st.gui_display.copy()

    diff_bar_update(scr)

    return scr


def gradient_rect(window, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pg.Surface((2, 2))  # tiny! 2x2 bitmap
    pg.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pg.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pg.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)


def diff_bar():
    scr = pg.Surface((diff_bar_dict["width"], diff_bar_dict["height"]))
    rect = scr.get_rect()
    gradient_rect(scr, (0, 255, 0), (255, 0, 0), rect)
    pg.draw.rect(scr, (0, 0, 0), scr.get_rect(), 4)
    st.gui_display.blit(scr, (diff_bar_dict["pos"][0], diff_bar_dict["pos"][1]))


def diff_bar_update(scr):
    x = Level.level.time / 200  # 200 - time to get the hardest difficulty
    pg.draw.rect(scr, (0, 0, 0), (diff_bar_dict["pos"][0] + diff_bar_dict["width"] * x, diff_bar_dict["pos"][1],
                                  diff_bar_dict["width"] * (1 - x), diff_bar_dict["height"]), 0)
