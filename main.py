import pygame as pg
import random, sys
from helper import Helper

helper = Helper()

SCREEN_X = 1280
SCREEN_Y = 720
FPS = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (0, 255, 255)

pg.init()
pg.mixer.init()
SCREEN = pg.display.set_mode((SCREEN_X, SCREEN_Y))
pg.display.set_caption("Neural Network Training")
clock = pg.time.Clock()

def load_asset(filename: str, size: tuple, format: str = ".png"):
    path = "assets/" + filename + format
    asset = pg.image.load(path)
    asset = pg.transform.scale(asset, size)
    return asset

try:
    main_bg = load_asset("main_bg", (SCREEN_X, SCREEN_Y))
    lower_bg = load_asset("lower_bg", (SCREEN_X, 206))
    ground = load_asset("ground", (SCREEN_X, 3))
    player = load_asset("player", (34, 42))
    player = pg.transform.rotate(player, -90)
    player_down = pg.transform.rotate(player, -45)
    player_up = pg.transform.rotate(player, 45)

except:
    print("Error loading assets")

currentPage = "game"
player_x = 200
player_y = 555

def game():
    global player, player_x, player_y, player_display, ascending, descending, on_roof, on_ground
    bg_shift = 0
    player_display = player
    ascending = False
    descending = False
    on_roof = False
    on_ground = False
    player_positions = []
    save_frame = 0
    raw_level = helper.load_map()
    helper.load_tiles(raw_level)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    player_display = player_up
                    if player_y - 30 < 555:
                        player_y -= 30
                    ascending = True
                    descending = False
            if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                player_display = player
                player_y += 30
                ascending = False
                descending = True

        # SCREEN.fill(BLACK)
        SCREEN.blit(main_bg, (bg_shift, 0))
        SCREEN.blit(main_bg, (SCREEN_X + bg_shift, 0))
        SCREEN.blit(lower_bg, (bg_shift, 597))
        SCREEN.blit(lower_bg, (SCREEN_X + bg_shift, 597))
        SCREEN.blit(ground, (0, 597))
        helper.draw_map(SCREEN)
        # SCREEN.blit(ground, (SCREEN_X + bg_shift, 550))

        if ascending:
            if player_y > 0:
                player_y -= 7
            else:
                player_y = 0
                player_display = player
                print("On Roof")
                on_roof = True
        elif player_y < 555:
            on_roof = False
            player_y += 7
            if player_y > 555:
                player_y = 555
            player_display = player_down
            if player_y > 540:
                player_display = player
        else:
            player_display = player
            descending = False
            ascending = False
            on_ground = True

        player_positions = [(x - 8, y) for x, y in player_positions if x - 8 >= -10]
        # for position in player_positions:
        #     x, y = position
        #     # rect = pg.rect.Rect(x + 28, y + 39, 20, 20)
        #     if ascending == True:
        #         pg.draw.circle(SCREEN, (0, 255, 255), (x, y), 10)
        #     else:
        #         pg.draw.circle(SCREEN, (0, 255, 255), (x, y), 10)
        #     # SCREEN.blit(rect)
        #     # pg.draw.rect(SCREEN, (255, 0, 0), rect)

        # if save_frame % 5 == 0:

        if ascending and on_roof == False:
            player_positions.append((player_x + 17, player_y + 35))
        elif descending:
            player_positions.append((player_x + 17, player_y + 19))
        elif on_roof:
            player_positions.append((player_x + 17, player_y + 23))
        else:
            player_positions.append((player_x + 17, player_y + 17))

        if len(player_positions) >= 2:
            pg.draw.lines(SCREEN, TEAL, False, player_positions, 20)

        player_mask = pg.mask.from_surface(player_display)
        for tile in helper.tile_list:
            tile_rect = tile[1]
            offset_x = tile_rect.x - player_x
            offset_y = tile_rect.y - player_y
            if player_mask.overlap(pg.mask.from_surface(tile[0]), (offset_x, offset_y)):
                print("GG")
                break
            if tile[1].x < -5000:
                print("You won")

        SCREEN.blit(player_display, (player_x, player_y))

        bg_shift -= 8
        if bg_shift <= -SCREEN_X:
            bg_shift = 0

        save_frame += 1

        pg.display.flip()
        clock.tick(FPS)

pages = {
    "game": game
}

def main():
    global currentPage
    while True:
        if currentPage in pages:
            nextPage = pages[currentPage]()
            currentPage = nextPage
        else:
            pg.quit()
            sys.exit()

if __name__ == "__main__":
    main()
