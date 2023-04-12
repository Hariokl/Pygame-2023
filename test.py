import pygame as pg


clock = pg.time.Clock()
FPS = 120
time = 0

while True:
    time += 1 / FPS
    print(f"\r{time}", end="")
    clock.tick(FPS)
