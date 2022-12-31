import pygame
import os
import sys


name = 'chars/midas.png'
tile_w = tile_h = 50
level = ['..........',
         '..........',
         '..........',
         '..........',
         '..........',
         '..........',
         '..........',
         '..........',
         '..........',
         '..........']


pygame.init()
size = w, h = 750, 300
pygame.display.set_caption('gg')
FPS = 50
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f'Файл с рисунком "{fullname}" не найден!')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is None:
        image.convert_alpha()
    else:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


ground = load_image('ground.png')


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = ground
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x, tile_h * pos_y)


class Char(pygame.sprite.Sprite):
    image = load_image(name)

    def __init__(self):
        super().__init__(player_group, all_sprites)
        self.image = Char.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(220, 210)


def generate(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            Tile(x, y)
            new_player = Char
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = w // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = h // 2 - (target.rect.y + target.rect.h // 2)


running = True
all_sprites = pygame.sprite.Group()
camera = Camera()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_g = pygame.sprite.Group()
player = None
player, level_x, level_y = generate(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.rect.x -= 50
                if pygame.sprite.spritecollideany(player, box_g):
                    player.rect.x += 50
            if event.key == pygame.K_RIGHT:
                player.rect.x += 50
                if pygame.sprite.spritecollideany(player, box_g):
                    player.rect.x -= 50
            if event.key == pygame.K_UP:
                player.rect.y -= 50
                if pygame.sprite.spritecollideany(player, box_g):
                    player.rect.y += 50
            if event.key == pygame.K_DOWN:
                player.rect.y += 50
                if pygame.sprite.spritecollideany(player, box_g):
                    player.rect.y -= 50
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)