import pygame
import random as rnd
import copy
import os


rand = 0


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    try:
        image = pygame.image.load(fullname)
    except AttributeError:
        print('error')
    else:
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image


class Board:  # Generate board 29x11
    def __init__(self):
        self.width = 29
        self.height = 11
        self.cell_size = 64
        self.left = 25
        self.top = 25
        self.table = [[0] * self.width for _ in range(self.height)]
        self.walls()
        self.destroyable_walls()
        self.table[0][0] = 0

    def walls(self):  # create undestroyable walls
        for i in (1, 3, 5, 7, 9):
            for j in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27):
                self.table[i][j] = 1

    def destroyable_walls(self):  # Create destroyable walls
        global rand
        coords_of_walls = []
        rand = rnd.randint(100, 300)
        for i in range(rand):
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

    def draw_everything(self):  # Draw obstacles
        for y in range(self.height):
            for x in range(self.width):
                if self.table[y][x] == 2:
                    Tile('destroyable_wall', self.left + self.cell_size * x, self.top + self.cell_size * y)
                    self.table[y][x] = 20
                if self.table[y][x] == 1:
                    Tile('wall', self.left + self.cell_size * x, self.top + self.cell_size * y)
                    self.table[y][x] = 10
                if self.table[y][x] == 0:
                    Tile('grass', self.left + self.cell_size * x, self.top + self.cell_size * y)

    def get_back(self, new_table):
        self.table = copy.deepcopy(new_table)

    def send_table(self):
        return self.table


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1900, 750
    pygame.display.set_caption('BomberMan')
    screen = pygame.display.set_mode(size)
    pl_sp_gr = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    destr_wall = pygame.sprite.Group()
    wall = pygame.sprite.Group()
    grass = pygame.sprite.Group()
    board = Board()
    tile_width = tile_height = 64
    cell_size = 64
    top = 25
    left = 25
    amount_of_bombs = 1

    tile_images = {  # Tile names and images
        'destroyable_wall': load_image('break_wall.png'),
        'wall': load_image('wall.png'),
        'grass': load_image('grass.png')
    }

    class Player(pygame.sprite.Sprite, Board):  # Responsible for movement
        image = load_image('bomberman.png')

        def __init__(self, *args):
            pygame.sprite.Sprite.__init__(self, *args)
            Board.__init__(self)
            self.player_image = Player.image
            self.rect = self.player_image.get_rect()
            self.rect.x = self.cell_size // 2.5
            self.rect.y = self.cell_size // 2.5

        def update(self, *args):
            self.new_table = args[0]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_DOWN]:
                if self.rect.y + self.cell_size < self.cell_size * self.height + self.top:
                    if self.new_table[(self.rect.y + int(self.cell_size * 0.6)) // self.cell_size][self.rect.x // self.cell_size] == 0:
                        self.rect.y += 60 / fps
            if pressed_key[pygame.K_UP]:
                if self.rect.y + self.cell_size > self.top + self.cell_size:
                    if self.new_table[(self.rect.y - int(self.cell_size * 0.25)) // self.cell_size][self.rect.x // self.cell_size] == 0:
                        self.rect.y -= 60 / fps
            if pressed_key[pygame.K_LEFT]:
                if self.rect.x > self.top:
                    if self.new_table[self.rect.y // self.cell_size][(self.rect.x - int(self.cell_size * 0.25)) // self.cell_size] == 0:
                        self.rect.x -= 60 / fps
            if pressed_key[pygame.K_RIGHT]:
                if self.rect.x + self.cell_size < self.left + self.cell_size * self.width:
                    if self.new_table[self.rect.y // self.cell_size][(self.rect.x + int(self.cell_size * 0.6)) // self.cell_size] == 0:
                        self.rect.x += 60 / fps

        def get_coords(self):  # Returns player coords
            return self.rect.x, self.rect.y

    class Bomb(pygame.sprite.Sprite):  # Responsible for bomb
        image = load_image('bomb.png')

        def __init__(self, group, table):
            super().__init__(group)
            self.cell_size = cell_size
            self.top = top
            self.width = 29
            self.height = 11
            self.left = left
            self.bomb_image = Bomb.image
            self.rect = self.bomb_image.get_rect()
            self.rect.x = -70
            self.rect.y = 0
            self.table = table

        def update(self, *args):  # Place bomb
            global amount_of_bombs
            self.coords = args[0][0] + self.cell_size + self.cell_size // 2, args[0][1] + self.cell_size // 2
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_z]:
                self.new_table = copy.deepcopy(self.table)
                if self.coords[0] in range(self.left, self.left + self.cell_size * self.width) \
                        and self.coords[1] in range(self.top, self.top + self.cell_size * self.height):
                    if self.new_table[self.coords[1] // self.cell_size][self.coords[0] // self.cell_size] == 0\
                            and amount_of_bombs != 0:
                        self.new_table[self.coords[1] // self.cell_size][self.coords[0] // self.cell_size] = 3
                        self.rect.x = (self.coords[0] // self.cell_size) * self.cell_size + self.left
                        self.rect.y = (self.coords[1] // self.cell_size) * self.cell_size + self.top
                        amount_of_bombs -= 1
                self.table = copy.deepcopy(self.new_table)

        def send_back(self):
            return self.table

    class Tile(pygame.sprite.Sprite):  # Draw tile
        def __init__(self, tile, pos_x, pos_y):
            self.left = left
            self.top = top
            if tile == 'destroyable_wall':
                super().__init__(destr_wall)
                self.image = tile_images[tile]
                self.rect = self.image.get_rect().move(pos_x, pos_y)
            elif tile == 'wall':
                super().__init__(wall)
                self.image = tile_images[tile]
                self.rect = self.image.get_rect().move(pos_x, pos_y)
            else:
                super().__init__(grass)
                self.image = tile_images[tile]
                self.rect = self.image.get_rect().move(pos_x, pos_y)

    player = Player(pl_sp_gr)
    bomb = Bomb(bomb_group, board.send_table())
    board.draw_everything()
    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        destr_wall.draw(screen)
        destr_wall.update()
        wall.draw(screen)
        wall.update()
        bomb_group.draw(screen)
        grass.draw(screen)
        grass.update()
        bomb.update(player.get_coords(), board.send_table())
        pl_sp_gr.draw(screen)
        player.update(board.send_table())
        board.get_back(bomb.send_back())
        pygame.display.flip()
    pygame.quit()