
class AIPlayer():
    def __init__(self, network):
        self.brain = network
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
        self.trail = []