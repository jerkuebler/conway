import random
import pygame
import sys


class Cell:
    def __init__(self, x, y, color, board, alive):
        self.x = x
        self.y = y
        self.alive = alive
        self.board = board
        self.color = color
        self.counter = 0

    def check_adjacent(self):

        living_neighbors = []
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                test_x = self.x + i
                test_y = self.y + j
                if i == 0 and j == 0:
                    pass
                elif self.board.side_len > test_x >= 0 and self.board.side_len > test_y >= 0:
                    cell = self.board.grid[test_x][test_y]
                    if cell.alive:
                        living_neighbors.append(cell)

        return living_neighbors

    def explode(self):
        self.counter = 0
        for i in range(-2, 3, 1):
            for j in range(-2, 3, 1):
                test_x = self.x + i
                test_y = self.y + j
                if i == 0 and j == 0:
                    pass
                elif self.board.side_len > test_x >= 0 and self.board.side_len > test_y >= 0:
                    self.board.grid[test_x][test_y].alive = False


def display_cells(pg_screen):
    for row in board.grid:
        for cell in row:
            cords = (int(step * cell.x) + 7, int(step * cell.y) + 7)
            if cell.alive:
                pygame.draw.circle(pg_screen, blue, cords, circle_size, 0)
            else:
                pygame.draw.circle(pg_screen, green, cords, circle_size, 0)


def cell_process(cell, pg_screen):
    cords = (int(step * cell.x) + 7, int(step * cell.y) + 7)
    adjacent = cell.check_adjacent()
    len_adj = len(adjacent)
    if cell.alive:
        pygame.draw.circle(pg_screen, cell.color, cords, circle_size, 0)
        if cell.counter > 25:
            cell.explode()
            pygame.draw.circle(pg_screen, red, cords, circle_size, 0)
        if len_adj < 2:
            cell.alive = False
            cell.counter = 0
        elif len_adj > 3:
            cell.alive = False
            cell.counter = 0
        else:
            cell.counter += 1
    else:
        pygame.draw.circle(pg_screen, green, cords, circle_size, 0)
        if len_adj == 3:
            cell.alive = True
            cell.color = (bounded_add(cell.color[0], random.randint(1, 40), 255),
                          bounded_add(cell.color[1], random.randint(1, 40), 255),
                          bounded_add(cell.color[2], random.randint(1, 40), 255))


def update_cells(pg_screen):

    for row in board.grid:
        for cell in row:
            cell_process(cell, pg_screen)


def bounded_add(a, b, bound):
    return (a + b) % bound


class Board:

    def __init__(self, side_len):
        self.side_len = side_len
        self.grid = []
        for i in range(side_len):
            self.grid.append([])
            for j in range(side_len):
                self.grid[i].append(Cell(i, j, blue, self, False))  # bool(random.getrandbits(1))


if __name__ == '__main__':

    # Create Window
    pygame.init()

    size = width, height = 800, 800
    black = 0, 0, 0
    blue = 0, 0, 255
    green = 50, 0, 50
    red = 255, 0, 0
    board_size = 200
    step = height / board_size
    circle_size = 3

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Click and drag to create cells. Press space to start!')
    # Initialize grid
    board = Board(board_size)

    # Begin ticks
    running = False
    painting = False

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                painting = True
                x = pygame.mouse.get_pos()[0] / step
                y = pygame.mouse.get_pos()[1] / step
                board.grid[int(x)][int(y)].alive = True

            if event.type == pygame.MOUSEBUTTONUP:
                painting = False

            if event.type == pygame.MOUSEMOTION and painting:
                x = pygame.mouse.get_pos()[0] / step
                y = pygame.mouse.get_pos()[1] / step
                board.grid[int(x)][int(y)].alive = True
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = True

        if running:
            update_cells(screen)
            pygame.time.wait(10)
        else:
            display_cells(screen)
            pygame.time.wait(10)

        pygame.display.update()
