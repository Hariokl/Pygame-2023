import pygame as pg
import settings as st


def spawn_mob(enemy):
    if enemy.time < 3:
        enemy.image.fill((0, 0, 0, 0))
        pg.draw.rect(enemy.image, (250, 100, int(enemy.time*50)), (0, 0, *enemy.rect.size), int(enemy.time*9+1))
        enemy.rect = enemy.image.get_rect()
        return None
    enemy.image.fill((250, 100, 100))
    enemy.rect = enemy.image.get_rect()
    enemy.spawn_stop = True

