import pygame
import math
from queue import PriorityQueue
import random

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows-1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm_astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()

    return False


def algorithm_bfs(draw, grid, start, end):
    visited = []
    queue = []
    came_from = {}

    visited.append(start)
    queue.append(start)

    while queue:
        start.make_start()
        end.make_end()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)
        current.make_open()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited:
                came_from[neighbor] = current  # Track the path
                visited.append(neighbor)
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def algorithm_dfs(draw, grid, start, end):
    stack = []
    came_from = {}
    visited = []

    stack.append(start)
    visited.append(start)

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()  # DFS uses stack (LIFO)
        current.make_open()

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and current != end:
                came_from[neighbor] = current  # Track the path
                visited.append(neighbor)
                stack.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def maze_generator(draw, grid, start):
    stack = []
    visited = set()

    stack.append(start)
    visited.add(start)

    total_cells = len(grid) * len(grid[0])  # Total number of cells in the grid

    def should_make_barrier(current, neighbor):
        if current.is_barrier():
            return random.random() < 0.6  # Higher probability near barriers
        else:
            return random.random() < 0.2  # Lower probability for random barriers

    while stack and len(visited) < total_cells:  # Continue until all cells are visited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()

        # Mark neighbors and randomly add barriers
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

                # Apply barrier logic
                if should_make_barrier(current, neighbor):
                    neighbor.make_barrier()

        draw()  # Redraw the grid at each step

    return True  # Maze generation complete


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(win, rows, width):  # draws grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    clock = pygame.time.Clock()
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None
    maze_generator_start = None
    maze_generator_end = None
    run = True
    finder_algorithm = algorithm_astar
    finder_algorithm_generator = None

    while run:
        clock.tick(300)
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not maze_generator_start:
                    maze_generator_start = spot
                    maze_generator_start.make_barrier()
                finder_algorithm = maze_generator

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    if finder_algorithm != maze_generator and start and end:
                        finder_algorithm_generator = finder_algorithm(lambda : draw(win,grid,ROWS,width),grid, start, end)
                    else:
                        finder_algorithm_generator = finder_algorithm(lambda : draw(win,grid,ROWS,width),grid, maze_generator_start)
                        finder_algorithm = algorithm_astar

                elif event.key == pygame.K_m and maze_generator_start:
                    finder_algorithm = maze_generator
                elif event.key == pygame.K_s and end:
                    finder_algorithm = algorithm_astar
                elif event.key == pygame.K_d and end:
                    finder_algorithm = algorithm_dfs
                elif event.key == pygame.K_b and end:
                    finder_algorithm = algorithm_bfs


                if event.key == pygame.K_c:
                    start = None
                    end = None
                    maze_generator_start = None
                    grid = make_grid(ROWS, width)
    pygame.quit()


main(WIN, WIDTH)
