import pygame as pg

class Helper():
    def __init__(self):
        self.TILE_SIZE = 64
        self.block_img_s = "assets/block.png"
        self.block_img = pg.transform.scale(pg.image.load("assets/block.png"), (40, 40))
        self.spike_img_s = "assets/spike.png"
        self.spike_img = pg.transform.scale(pg.image.load("assets/spike.png"), (40, 40))

        self.tile_list = []

    def load_map(self, mapName="assets/levels/level_0.txt"):
        try:
            with open(mapName, "r") as file:
                level = [list(line.strip()) for line in file.readlines()]
                return level
        except FileNotFoundError:
            print(mapName)
            return 0
    

    def draw_map(self, SCREEN):
        for tile in self.tile_list:
            tile[1].x -= 8
            SCREEN.blit(tile[0], tile[1])
    
    def get_image(self, tile, source):
        if source:
            if tile == "1":
                return self.block_img_s
            elif tile == "2":
                return self.spike_img_s
        else:
            if tile == "1":
                return self.block_img
            elif tile == "2":
                return self.spike_img
    

    def load_tiles(self, level):
        self.tile_list = []
        for row_index, row in enumerate(level):
            for col_index, tile in enumerate(row):
                if tile == "1" or tile == "2":
                    image = self.get_image(tile, False)
                    img = pg.transform.scale(image, (40, 40))
                    img_rect = pg.Rect(col_index * 40, row_index * 40, 40, 40)
                    tile = (img, img_rect, self.get_image(tile, True))
                    self.tile_list.append(tile)