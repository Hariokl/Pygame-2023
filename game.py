import pygame as pg
from numpy import sqrt

import settings as st
from map import Map


class Game:
    def __init__(self):
        # was forced to put import here since it's the easiest way to avoid error
        from player import Player
        self.clock = pg.time.Clock()
        self.map = Map()
        self.player = Player()
        self.enemies = []
        self.run()

    # I think this run function is the cleanest one in my whole life :D
    def run(self):
        while True:
            check_event(self)

            st.display.fill((0, 0, 0))
            st.all_sprites.update()
            st.all_sprites.draw(st.display)

            pg.display.flip()
            self.clock.tick(st.FPS)
            pg.display.set_caption(str(int(self.clock.get_fps())))


# here I check every event that has occurred, quite straightforwardly, isn't it?
def check_event(game):
    for event in pg.event.get():
        # THE MOST DIFFICULT IF-STATEMENT TO UNDERSTAND
        if event.type == pg.QUIT:
            exit()

        # shoot!
        # need to change this, so I should shoot only when left mouse button is down or pressed
        if event.type == pg.MOUSEBUTTONDOWN:
            game.player.shoot_bool = True

        # don't shoot!
        if event.type == pg.MOUSEBUTTONUP:
            game.player.shoot_bool = False

        # starting the movement
        if event.type == pg.KEYDOWN:
            x = (event.key == pg.K_d) - (event.key == pg.K_a) + game.player.running[0]
            y = (event.key == pg.K_s) - (event.key == pg.K_w) + game.player.running[1]
            if x != 0 and y != 0:
                x = sqrt(2) / 2 * x
                y = sqrt(2) / 2 * y
            game.player.running = x, y
            print(game.player.running)

        # continuing the movement
        if event.type == pg.KEYUP:
            x = 0 if event.key == pg.K_d or event.key == pg.K_a else game.player.running[0]
            y = 0 if event.key == pg.K_s or event.key == pg.K_w else game.player.running[1]

            # if lagging comment this section (but it's NOT recommended, since it'll destroy cool movement experience)
            keys = pg.key.get_pressed()
            if keys[119]:
                y += -1
            if keys[115]:
                y += +1
            if keys[97]:
                x += -1
            if keys[100]:
                x += +1
            x, y = max(min(x, 1), -1), max(min(y, 1), -1)

            game.player.running = x, y

    # move if you can >:)
    if game.player.running != (0, 0):
        game.player.move(*game.player.running)

    # SHOOOOOOOOOOOT!!!!! >:D
    if game.player.shoot_bool and game.player.weapon.countdown == 0:
        game.player.shoot()
