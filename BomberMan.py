import pygame
import random as rnd
import copy
import os


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


def load_level(filename):
    filename = "pictures/" + filename + '.txt'
    # читаем уровень, убирая символы перевода строки
    print(filename)
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


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


    def generate_level(level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile('grass', x, y)
                elif level[y][x] == '#':
                    Tile('wall', x, y)
                elif level[y][x] == '@':
                    Tile('grass', x, y)
                    new_player = Player(pl_sp_gr, x, y)
                    level[y][x] = '.'
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


    class Player(pygame.sprite.Sprite):  # Responsible for movement
        image = load_image('bomberman.png')

        def __init__(self, group, pos_x, pos_y):
            super().__init__(group)
            self.cell_size = cell_size
            self.top = top
            self.left = left
            self.height = 11
            self.width = 29
            self.player_image = Player.image
            self.rect = self.player_image.get_rect()
            self.rect.x = pos_x
            self.rect.y = pos_y

        def update(self, *args):
            self.new_table = args[0]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_DOWN]:
                if not pygame.sprite.spritecollideany(self, wall):
                    self.rect.y += 60 / FPS
                else:
                    self.rect.y -= 1
            if pressed_key[pygame.K_UP]:
                if not pygame.sprite.spritecollideany(self, wall):
                    self.rect.y -= 60 / FPS
                else:
                    self.rect.y += 1
            if pressed_key[pygame.K_LEFT]:
                if not pygame.sprite.spritecollideany(self, wall):
                    self.rect.x -= 60 / FPS
                else:
                    self.rect.x += 1
            if pressed_key[pygame.K_RIGHT]:
                if not pygame.sprite.spritecollideany(self, wall):
                    self.rect.x += 60 / FPS
                else:
                    self.rect.x -= 1

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
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)
            elif tile == 'wall':
                super().__init__(wall)
                self.image = tile_images[tile]
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)
            elif tile == 'grass':
                super().__init__(grass)
                self.image = tile_images[tile]
                self.rect = self.image.get_rect().move(
                    tile_width * pos_x, tile_height * pos_y)

    level_map = load_level('map')
    player, level_x, level_y = generate_level(level_map)
    bomb = Bomb(bomb_group, level_map)
    running = True
    FPS = 60
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        destr_wall.draw(screen)
        destr_wall.update()
        wall.draw(screen)
        wall.update()
        grass.draw(screen)
        grass.update()
        bomb_group.draw(screen)
        bomb.update(player.get_coords())
        pl_sp_gr.draw(screen)
        player.update(level_map)
        pygame.display.flip()
    pygame.quit()