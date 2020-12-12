import pygame
import random as rnd
import copy


class Board:  # Generate board 29x11
    def __init__(self):
        self.width = 29
        self.height = 11
        self.cell_size = 64
        self.left = 25
        self.top = 25
        self.table = [[0] * self.width for _ in range(self.height)]
        self.table[0][0] = 3
        self.walls()
        self.destroyable_walls()

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                if self.table[i][j] == 0:
                    pygame.draw.rect(screen, pygame.Color('white'), (self.left + self.cell_size * j, self.top +
                                                                     self.cell_size * i, self.cell_size, self.cell_size),
                                     0 if self.table[i][j] else 1)
                elif self.table[i][j] == 1:
                    pygame.draw.rect(screen, pygame.Color('white'), (self.left + self.cell_size * j, self.top +
                                                                     self.cell_size * i, self.cell_size,
                                                                     self.cell_size),
                                     0 if self.table[i][j] else 1)
                elif self.table[i][j] == 2:
                    pygame.draw.rect(screen, pygame.Color('brown'), ((self.left + self.cell_size * j) + 1,
                                                                     (self.top + self.cell_size * i) + 1,
                                                                     self.cell_size, self.cell_size), 0)
                    pygame.draw.rect(screen, pygame.Color('white'), (self.left + self.cell_size * j, self.top +
                                                                     self.cell_size * i, self.cell_size, self.cell_size)
                                     , 1)
                elif self.table[i][j] == 3:
                    pygame.draw.line(screen, pygame.Color('blue'), (self.left + self.cell_size * j, self.top +
                                                                    self.cell_size * i),
                                     (self.cell_size + self.left + self.cell_size * j,
                                      self.cell_size + self.top + self.cell_size * i), 5)
                    pygame.draw.rect(screen, pygame.Color('white'), (self.left + self.cell_size * j, self.top +
                                                                     self.cell_size * i, self.cell_size, self.cell_size)
                                     , 1)
                elif self.table[i][j] == 4:
                    pygame.draw.circle(screen, pygame.Color('grey'), (self.cell_size // 2 + self.left +
                                                                      self.cell_size * j,
                                                                      self.cell_size // 2 + self.top +
                                                                      self.cell_size * i), self.cell_size // 2.5)
                    pygame.draw.rect(screen, pygame.Color('white'), (self.left + self.cell_size * j, self.top +
                                                                     self.cell_size * i, self.cell_size,
                                                                     self.cell_size), 1)

    def walls(self):
        for i in (1, 3, 5, 7, 9):
            for j in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27):
                self.table[i][j] = 1

    def destroyable_walls(self):
        coords_of_walls = []
        for i in range(rnd.randint(100, 300)):
            y = rnd.randint(0, 10)
            x = rnd.randint(0, 28)
            while (x, y) in coords_of_walls:
                y = rnd.randint(0, 10)
                x = rnd.randint(0, 28)
            if (x, y) not in coords_of_walls:
                coords_of_walls.append((x, y))
                if self.table[y][x] == 0:
                    if y == 0 and x == 1 or y == 1 and x == 0:
                        self.table[y][x] = 0
                    else:
                        self.table[y][x] = 2


class Player(Board):  # Responsible for movement and placing bombs
    def __init__(self):
        super().__init__()

    def move_down(self):
        self.new_table = copy.deepcopy(self.table)
        x, y = None, None
        for i in range(self.height):
            for j in range(self.width):
                if self.new_table[i][j] == 3:
                    x, y = j, i
        if y is not None:
            if y != len(self.new_table) - 1:
                if self.new_table[y + 1][x] == 0:
                    self.new_table[y][x] = 0
                    self.new_table[y + 1][x] = 3
        self.table = copy.deepcopy(self.new_table)

    def move_up(self):
        self.new_table = copy.deepcopy(self.table)
        x, y = None, None
        for i in range(self.height):
            for j in range(self.width):
                if self.new_table[i][j] == 3:
                    x, y = j, i
        if y is not None:
            if self.new_table[y - 1][x] == 0:
                if y - 1 in range(len(self.new_table) - 1):
                    self.new_table[y][x] = 0
                    self.new_table[y - 1][x] = 3
        self.table = copy.deepcopy(self.new_table)

    def move_left(self):
        self.new_table = copy.deepcopy(self.table)
        x, y = None, None
        for i in range(self.height):
            for j in range(self.width):
                if self.new_table[i][j] == 3:
                    x, y = j, i
        if x is not None:
            if self.new_table[y][x - 1] == 0:
                if x - 1 in range(len(self.new_table[y]) - 1):
                    self.new_table[y][x] = 0
                    self.new_table[y][x - 1] = 3
        self.table = copy.deepcopy(self.new_table)

    def move_right(self):
        self.new_table = copy.deepcopy(self.table)
        x, y = None, None
        for i in range(self.height):
            for j in range(self.width):
                if self.new_table[i][j] == 3:
                    x, y = j, i
        if x is not None:
            if x != len(self.new_table[y]) - 1:
                if self.new_table[y][x + 1] == 0:
                    self.new_table[y][x] = 0
                    self.new_table[y][x + 1] = 3
        self.table = copy.deepcopy(self.new_table)

    def place_bomb(self, direction):
        self.new_table = copy.deepcopy(self.table)
        x, y = None, None
        for i in range(self.height):
            for j in range(self.width):
                if self.new_table[i][j] == 3:
                    x, y = j, i
        if direction == 'down' or direction == 'up':
            if y is not None:
                if direction == 'down':
                    if y != len(self.table) - 1:
                        if self.new_table[y + 1][x] == 0:
                            self.new_table[y + 1][x] = 4
                else:
                    if y != 0:
                        if self.new_table[y - 1][x] == 0:
                            self.new_table[y - 1][x] = 4
        else:
            if x is not None:
                if direction == 'left':
                    if x != 0:
                        if self.new_table[y][x - 1] == 0:
                            self.new_table[y][x - 1] = 4
                else:
                    if x != len(self.table[y]) - 1:
                        if self.new_table[y][x + 1] == 0:
                            self.new_table[y][x + 1] = 4
        self.table = copy.deepcopy(self.new_table)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1900, 750
    pygame.display.set_caption('BomberMan')
    screen = pygame.display.set_mode(size)
    board = Board()
    player = Player()
    running = True
    direction = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    direction = 'down'
                    player.move_down()
                if event.key == pygame.K_UP:
                    direction = 'up'
                    player.move_up()
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    player.move_left()
                if event.key == pygame.K_RIGHT:
                    direction = 'right'
                    player.move_right()
                if event.key == pygame.K_z:
                    player.place_bomb(direction)
        screen.fill((0, 0, 0))
        player.render(screen)
        pygame.display.flip()
    pygame.quit()