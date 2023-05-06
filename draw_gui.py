import pygame as pg
import settings as st
import levels as lvls
import enemy


def setup():
    global diff_bar_dict
    diff_bar_dict = {"wave_time": 3, "waveWH": (None, None),
                     "killed_enemy_count": ((st.WIDTH / 40, st.WIDTH / 30), (st.WIDTH / 20 + st.WIDTH / 20, st.WIDTH / 30))}


def update():
    scr = st.gui_display.copy()

    killed_enemy_count(scr)
    if diff_bar_dict["wave_time"] > 0:
        wave_update(scr)
    else:
        diff_bar_dict["waveWH"] = (None, None)
    return scr


def wave_update(scr):
    diff_bar_dict["wave_time"] -= st.TICK
    wave = lvls.Level.level.wave

    text_surface = st.font60.render(f"Wave {wave}", True, (250, 250, 250))  # , min(255 - diff_bar_dict["wave_time"] * 85, 0)
    text_surface.set_alpha(max(diff_bar_dict["wave_time"] * 85, 0))

    if diff_bar_dict["waveWH"] == (None, None):
        diff_bar_dict["waveWH"] = st.WIDTH // 2 - text_surface.get_width() // 2, st.HEIGHT // 2 - text_surface.get_height() // 2

    scr.blit(text_surface, diff_bar_dict["waveWH"])


def killed_enemy_count(scr):
    killed_enemy = enemy.Enemy.number_of_killed
    all_enemy = lvls.Level.level.max_number_of_monsters_per_wave
    scr1 = pg.Surface((st.WIDTH / 20, st.WIDTH / 20))
    scr1.fill((230, 100, 100))

    text_surface = st.font30.render(f"{killed_enemy}/{all_enemy}", False, (230, 100, 100))
    pos1, pos2 = diff_bar_dict["killed_enemy_count"]

    scr.blit(scr1, pos1)
    scr.blit(text_surface, pos2)







#
# def gradient_rect(window, left_colour, right_colour, target_rect):
#     """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
#     colour_rect = pg.Surface((2, 2))  # tiny! 2x2 bitmap
#     pg.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
#     pg.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
#     colour_rect = pg.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
#     window.blit(colour_rect, target_rect)
#
#
# def diff_bar():
#     scr = pg.Surface((diff_bar_dict["width"], diff_bar_dict["height"]))
#     rect = scr.get_rect()
#     gradient_rect(scr, (0, 255, 0), (255, 0, 0), rect)
#     pg.draw.rect(scr, (0, 0, 0), scr.get_rect(), 4)
#     st.gui_display.blit(scr, (diff_bar_dict["pos"][0], diff_bar_dict["pos"][1]))
#
#
# def diff_bar_update(scr):
#     x = Level.level.time / 200  # 200 - time to get the hardest difficulty
#     pg.draw.rect(scr, (0, 0, 0), (diff_bar_dict["pos"][0] + diff_bar_dict["width"] * x, diff_bar_dict["pos"][1],
#                                   diff_bar_dict["width"] * (1 - x), diff_bar_dict["height"]), 0)
