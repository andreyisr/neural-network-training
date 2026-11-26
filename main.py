import pygame as pg
import numpy as np
import sys, math
from helper import Helper
from neural_network import NeuralNetwork

helper = Helper()

# Defining Constant Variables
SCREEN_X = 1280
SCREEN_Y = 720
FPS = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TEAL = (0, 255, 255)

# Neural Network variables
population_size = 1000
breeding_amount = 10
mutation_amount = 0.2

# Initiating Pygame with all parameters
pg.init()
pg.mixer.init()
SCREEN = pg.display.set_mode((SCREEN_X, SCREEN_Y))
pg.display.set_caption("Neural Network Training")
clock = pg.time.Clock()

# Loading in all assets
def load_asset(filename: str, size: tuple, format: str = ".png"):
    path = "assets/" + filename + format
    asset = pg.image.load(path)
    asset = pg.transform.scale(asset, size)
    return asset

try:
    main_bg = load_asset("main_bg", (SCREEN_X, SCREEN_Y))
    lower_bg = load_asset("lower_bg", (SCREEN_X, 206))
    ground = load_asset("ground", (SCREEN_X, 3))
    player = load_asset("player", (37, 30))
    player_down = load_asset("player_down", (48, 45))
    player_up = load_asset("player_up", (36, 34))

except:
    print("Error loading assets")

currentPage = "game"
player_x = 200
player_y = 555

epoch = 0
ray_cos = []
ray_sin = []
for ray in [90, 70, 45, 0, -45, -70, -90]:
    radians = math.radians(ray)
    ray_cos.append(math.cos(radians))
    ray_sin.append(math.sin(radians))

font = pg.font.Font(None, 36)


class AIPlayer():
    def __init__(self, network):
        self.brain = network
        self.save_frame = 0
        self.x = 200
        self.y = 555
        self.alive = True
        self.score = 0

        self.ascending = False
        self.descending = False
        self.on_roof = False
        self.on_ground = False
        self.on_block = False
        self.ceiling_attached = False
        self.block_on = None
        self.display = player
        self.player_positions = []

        self.space_pressed = False
        self.frames_after_landing_left = 0

def start_generation(population_size):
    # raw_level = helper.load_map()
    # helper.load_tiles(raw_level)

    network_list = []
    for network in range(population_size):
        network_list.append(AIPlayer(NeuralNetwork(None, None, epoch=epoch)))

    return network_list

def get_game_inputs(x, y, save_frame, raw_level):
    column = (save_frame * 8 + x) / 40
    row = y / 40
    ray_angles = [90, 70, 45, 0, -45, -70, -90]
    distance = 10
    ray_values = []
    for index, ray in enumerate(ray_angles):
        for step in range(20):
            step_x = ray_cos[index] * distance * step
            step_y = ray_sin[index] * distance * step
            temp_row = math.floor((y + step_y) / 40)
            temp_column = math.floor((save_frame * 8 + (x + step_x)) / 40)

            # Checks that the ray endpoint is within bounds (on screen), otherwise I can't access tile at that potition
            if 0 > temp_row >= 15 and 0 > temp_column >= len(raw_level[0]):
                if (raw_level[temp_row][temp_column] == '1' or raw_level[temp_row][temp_column] == '2'):
                    ray_values.append(step / 20)
                    break
        else:
            ray_values.append(1.0)

    return ray_values



# Main Game loop
def game():
    # global player, player_x, player_y, player_display, ascending, descending, on_roof, on_ground, found_next_block, block_on

    # Defining variables
    # player_display = player
    # ascending = False
    # descending = False
    # on_roof = False
    # on_ground = False
    # on_block = False
    # ceiling_attached = False
    # block_on = None
    # player_positions = []
    # space_pressed = False
    save_frame = 0
    bg_shift = 0

    raw_level = helper.load_map()
    helper.load_tiles(raw_level)
    level_length = helper.get_level_length(raw_level) * 5
    # frames_after_landing_left = 0
    progress_percentage = 0
    networks = start_generation(population_size)

    # Creating Initial Population
    # epoch = 0
    # population = [NeuralNetwork(epoch=epoch) for i in range(population_size)]

    while True:

        # Event listener
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # if event.type == pg.KEYDOWN:
            #     # Pressing down 'Space'
            #     if event.key == pg.K_SPACE:
            #         space_pressed = True
            #         player_display = player_up
            #         # if player_y - 30 < 555:
            #             # player_y -= 30
            #         ascending = True
            #         descending = False
            # # Releasing 'Space'
            # if event.type == pg.KEYUP and event.key == pg.K_SPACE:
            #     player_display = player
            #     # player_y += 30
            #     ascending = False
            #     descending = True
            #     space_pressed = False

        # Displaying all background assets
        SCREEN.blit(main_bg, (bg_shift, 0))
        SCREEN.blit(main_bg, (SCREEN_X + bg_shift, 0))
        SCREEN.blit(lower_bg, (bg_shift, 597))
        SCREEN.blit(lower_bg, (SCREEN_X + bg_shift, 597))
        SCREEN.blit(ground, (0, 597))
        helper.draw_map(SCREEN)
        # SCREEN.blit(ground, (SCREEN_X + bg_shift, 550))


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


        # if ascending and on_roof == False:
        #     player_positions.append((player_x + 17, player_y + 35))
        # elif descending:
        #     player_positions.append((player_x + 17, player_y + 19))
        # if on_roof:
        #     player_positions.append((player_x + 17, player_y + 23))
        # else:

        # pg.draw.circle(SCREEN, (255, 0, 0), (player_x + 15, player_y + 15), 3)
        # pg.draw.circle(SCREEN, (255, 0, 0), (player_x, player_y), 3)
        # pg.draw.rect(SCREEN, (255, 0, 0), player_display.get_rect(topleft=(player_x, player_y)), 2)

        
        for network in networks:
            if network.alive == False:
                continue
            # Input handling of specific networks
            inputs = get_game_inputs(network.x, network.y, save_frame, raw_level)
            action = network.brain.predict(np.array(inputs))
            if action == 1:
                network.space_pressed = True
                network.display = player_up
                network.ascending = True
                network.descending = False
            elif action == 0:
                network.display = player
                network.ascending = False
                network.descending = True
                network.space_pressed = False

            # Movement/Collision logic
            if network.ceiling_attached:
                if network.space_pressed and network.block_on is not None:
                    network.y = network.block_on[1].y + 45
                    network.display = player
                    network.ascending = False
                    network.descending = False
                elif network.space_pressed:
                    network.ceiling_attached = False
                    network.on_block = False
                    network.block_on = None
                    network.ascending = True
                else:
                    network.ceiling_attached = False
                    network.on_block = False
                    network.block_on = None
                    network.descending = True

            if not network.ceiling_attached:
                if network.ascending:
                    if network.y > 0:
                        network.y -= 7
                        network.on_block = False
                        network.block_on = None
                    else:
                        network.y = 0
                        network.display = player
                        network.on_roof = True
                elif not network.on_block and network.y < 565:
                    network.on_roof = False
                    network.y += 7
                    if network.y > 565:
                        network.y = 565
                    network.display = player_down
                    if network.y > 550:
                        network.display = player
                elif not network.on_block:
                    network.display = player
                    network.descending = False
                    network.ascending = False
                    network.on_ground = True
        
            # Trail position management (deleting if offscreen by more than 10px)
            network.player_positions = [(x - 8, y) for x, y in network.player_positions if x - 8 >= -10]

            # Accelerated fly-in of character before start of level
            if network.save_frame < 60:
                network.x = network.save_frame * 3.5 - 6.5
            
            # Saving player position
            if network.frames_after_landing_left == 0:
                network.player_positions.append((network.x + 15, network.y + 15))
            else:
                network.frames_after_landing_left -= 1

            if len(network.player_positions) >= 2:
                pg.draw.lines(SCREEN, TEAL, False, network.player_positions, 20)

            # for tile in helper.tile_list:
            #     tile_rect = tile[1]
            #     offset_x = tile_rect.x - player_x
            #     offset_y = tile_rect.y - player_y
            #     if player_mask.overlap(pg.mask.from_surface(tile[0]), (offset_x, offset_y)):
            #         print("GG")
            #         break
            #     if tile[1].x < -5000:
            #         print("You won")

            # Checking next block to see whether ground below character exists
            network.found_next_block = False
            if network.on_block and network.block_on is not None:
                if network.ceiling_attached:
                    block_passed = network.block_on[1].x + 40 <= network.x
                else:
                    block_passed = network.block_on[1].x + 40 <= network.x
                if block_passed:
                    for tile in helper.tile_list:
                        if tile[1].y == network.block_on[1].y and network.block_on[1].x + 40 == tile[1].x and tile[2] != "assets/spike.png":
                            network.block_on = tile
                            network.found_next_block = True

                    if not network.found_next_block:
                        network.on_block = False
                        network.ceiling_attached = False
                        network.block_on = None
                        if network.space_pressed:
                            network.ascending = True
                            network.descending = False
                        else:
                            network.descending = True

            # Character block collision
            for tile in helper.tile_list:
                tile_rect = tile[1]
                offset_x = tile_rect.x - network.x
                offset_y = tile_rect.y - network.y
                offset_x_bottom = tile_rect.x - network.x
                offset_y_bottom = network.y - (tile_rect.y + 40)
                if network.ascending and 10 > offset_y_bottom > -5 and 40 > offset_x_bottom > 0 and tile[2] != "assets/spike.png":
                    network.display = player
                    network.descending = False
                    network.ascending = False
                    network.on_ground = True
                    network.on_block = True
                    network.ceiling_attached = True
                    network.block_on = tile
                    network.y = tile_rect.y + 45
                if not network.ascending and 45 > offset_y > 25 and 40 > offset_x > -5 and tile[2] != "assets/spike.png":
                    network.display = player
                    network.descending = False
                    network.ascending = False
                    network.on_ground = True
                    if not network.on_block:
                        network.frames_after_landing_left = 1
                    network.on_block = True
                    network.block_on = tile
                    network.y = tile_rect.y - player.get_height()
                network_rect = network.display.get_rect(topleft=(network.x,network.y))
                if network_rect.colliderect(tile[1]) and (tile[2] == "assets/spike.png" or tile_rect.top < network.y + network.display.get_height() / 2 < tile_rect.bottom):
                    network.alive = False
                # if tile[1].x < -5000: 
                #     # print("You won")
                #     continue

            # Managing player sprites based on movement
            if network.display == player_up:
                SCREEN.blit(network.display, (network.x, network.y - 4))
            else:
                SCREEN.blit(network.display, (network.x, network.y))

            if network.alive == True:
                network.score += 1
            network.save_frame += 1


        # Progress Bar
        temp_surface = pg.Surface((400, 40), pg.SRCALPHA)
        pg.draw.rect(temp_surface, (0, 0, 0, 200), (0, 0, 400, 40), border_radius=5)
        SCREEN.blit(temp_surface, (420, 0))
        # pg.draw.rect(SCREEN, (0, 0, 0), (420, 0, 400, 40))
        progress_percentage = min(max((save_frame - 20)/(level_length - 20), 0), 1)
        if progress_percentage == 1:
            sys.exit()
            pg.quit()
        else:
            networks_alive = len(networks)
            for network in networks:
                if network.alive == False:
                    networks_alive -= 1
            if networks_alive == 0:
                sys.exit()
                pg.quit()
        print(progress_percentage)
        pg.draw.rect(SCREEN, (255, 255, 255, 128), (510, 10, 300, 20), 4, 45)
        pg.draw.rect(SCREEN, (255, 255, 255), (514, 14, 3, 12))
        pg.draw.rect(SCREEN, (255, 255, 255), (517, 14, progress_percentage * 293, 16))
        text = font.render(f'{round(progress_percentage * 100)} %', True, (255, 255, 255))
        SCREEN.blit(text, (440, 10))

        print("Networks alive:", networks_alive)
        
        # Shifting background and blocks by 8
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
