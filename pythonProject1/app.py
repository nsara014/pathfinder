import pygame
from settings import *
from astar import *
from Spot import *


class App:
    def __init__(self):
        self.win = pygame.display.set_mode((GRID_WIDTH, GRID_WIDTH))
        self.game_caption = "A* Path Finding Algorithm"
        self.running = True
        self.start = None
        self.end = None
        self.rows = ROWS
        self.width = GRID_WIDTH
        self.grid = []
        self.dummy = [[1, 2, 3, ], [2, 3, 4]]

    def make_grid(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                spot = Spot(i, j, gap, self.rows)
                self.grid[i].append(spot)

    def draw(self):
        self.win.fill(WHITE)

        for row in self.grid:
            for spot in row:
                spot.draw(self.win)

        self.draw_grid()
        pygame.display.update()

    def draw_grid(self):
        gap = self.width // self.rows
        for i in range(self.rows):
            pygame.draw.line(self.win, GREY, (0, i * gap), (self.width, i * gap))
            for j in range(self.rows):
                pygame.draw.line(self.win, GREY, (j * gap, 0), (j * gap, self.width))

    def get_clicked_pos(self, pos):
        gap = self.width // self.rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    def run(self):
        pygame.display.set_caption(self.game_caption)
        self.make_grid()

        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if pygame.mouse.get_pressed()[0]:  # LEFT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    print(self.grid)
                    spot = self.grid[row][col]
                    if not self.start and spot != self.end:
                        self.start = spot
                        self.start.make_start()

                    elif not self.end and spot != self.start:
                        self.end = spot
                        self.end.make_end()

                    elif spot != self.end and spot != self.start:
                        spot.make_barrier()

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos)
                    spot = self.grid[row][col]
                    spot.reset()
                    if spot == self.start:
                        self.start = None
                    elif spot == self.end:
                        self.end = None

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        for row in self.grid:
                            for spot in row:
                                spot.update_neighbors(self.grid)

                        astaralgorithm(lambda: self.draw(), self.grid, self.start, self.end)

                    if event.key == pygame.K_c:
                        self.start = None
                        self.end = None
                        self.make_grid()
        pygame.quit()
