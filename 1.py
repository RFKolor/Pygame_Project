import pygame
import os
import sys
import random

name = 'level1.txt'
char_name = 'midas'

pygame.init()
size = w, h = 500, 850
pygame.display.set_caption("Reverenge Georgis")
FPS = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
#пока босс жив переменна true, когда босс повержен переменная меняется на false,используется для
#экрана окончания
georgis = True
spavnpoint = 0
enemis = []
enemis_speed = 1
damage = 5


class Button:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.button_click = pygame.mixer.Sound("data/button.wav")

    def draw(self, x, y, text, function=None):
        # function передает вызов функции или саму функцию,допустим начало игры или выход
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, (0, 0, 255), (x, y, self.width, self.height), 0)
        print_text(text, x + 10, y + 10, (255, 255, 255))
        if x < mouse_pos[0] < x + self.width:
            if y < mouse_pos[1] < y + self.height:
                if mouse_clicked[0] == 1:
                    pygame.mixer.Sound.play(self.button_click)
                    pygame.time.delay(500)
                    if function is not None:
                        if function == "exit":
                            terminate()
                        elif function == "play":
                            play()
                        elif function == "menu":
                            show_menu()


#функция для печатания текста
def print_text(text, x, y, font_color=(0, 0, 0), font_size=50):
    font_type = pygame.font.SysFont('arial', font_size)
    message = font_type.render(text, True, font_color)
    screen.blit(message, (x, y))


#меню окончания игры
def end_game():
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    image_background = pygame.image.load("data/menu_bg.jpg").convert_alpha()
    show = True
    start_game_button = Button(150, 70)
    quit_game_button = Button(100, 70)
    if georgis:
        text = "You Win!"
        color = (0, 255, 0)
    else:
        text = "You Lose"
        color = (255, 0, 0)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()
                if event.key == pygame.K_RETURN:
                    play()
        screen.blit(image_background, (0, 0))
        print_text(text, 130, 180, color, 70)
        start_game_button.draw(0, 430, "Restart", "play")
        quit_game_button.draw(400, 430, "Quit", "exit")
        pygame.display.flip()


#главное меню
def show_menu():
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    image_background = pygame.image.load("data/menu_bg.jpg").convert_alpha()
    show = True
    start_game_button = Button(230, 70)
    quit_game_button = Button(100, 70)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play()
        screen.blit(image_background, (0, 0))
        print_text("Reverenge Georgis", 0, 0, (243, 165, 5), 70)
        start_game_button.draw(120, 100, "Start Game", "play")
        quit_game_button.draw(180, 300, "Quit", "exit")
        pygame.display.flip()


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


tile = load_image('ground.png')
cube_images = [load_image('enemis/cube.png'), load_image('enemis/cube1.png'),
               load_image('enemis/cube2.png'), load_image('enemis/cube3.png')]
if char_name == 'midas':
    player_images = [load_image('chars/midas.png'), load_image('chars/midas1-3.png'),
                     load_image('chars/midas2.png'), load_image('chars/midas1-3.png')]
tile_w = tile_h = 50


def load_level(filename):
    filename = 'data/' + filename
    with open(filename, 'r') as file:
        map_level = list(map(str.strip, file.readlines()))
    max_widht = max(map(len, map_level))
    return list(map(lambda x: x.ljust(max_widht, '.'), map_level))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(box_g)
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x, tile_h * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, frame):
        super().__init__(player_group, all_sprites)
        self.heals = 1000
        self.image = player_images[frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x + 15, tile_h * pos_y + 5)


class Cube(pygame.sprite.Sprite):
    def __init__(self, frame):
        super().__init__(enemi_group, all_sprites)
        self.live = True
        self.damage = 1
        self.image = cube_images[frame]
        self.rect = self.image.get_rect()
        self.heals = 1
        if random.choice((0, 1)) == 1:
            self.rect = self.rect.move(random.choice((-25, 500)), random.randint(-25, 851))
        else:
            self.rect = self.rect.move(random.randint(-25, 500), random.choice((-25, 851)))

    def mislitelniy_process(self):
        if self.heals > 0:
            rastoyanie_x = self.rect.x - player.rect.x
            rastoyanie_y = self.rect.y - player.rect.y
            if rastoyanie_y != 0 and rastoyanie_x != 0:
                if rastoyanie_x > rastoyanie_y:
                    koef = abs(rastoyanie_x) / abs(rastoyanie_y)
                    if koef < 1:
                        koef = 1
                    self.rect = self.rect.move(enemis_speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)),
                                               enemis_speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)) / koef)
                elif rastoyanie_x < rastoyanie_y:
                    koef = abs(rastoyanie_y) / abs(rastoyanie_x)
                    if koef < 1:
                        koef = 1
                    self.rect = self.rect.move(enemis_speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)) / koef,
                                               enemis_speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)))
                else:
                    self.rect = self.rect.move(enemis_speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)),
                                               enemis_speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)))
            elif rastoyanie_x == 0 and rastoyanie_y != 0:
                self.rect.y += enemis_speed * -(rastoyanie_y / abs(rastoyanie_y))
            elif rastoyanie_y == 0 and rastoyanie_x != 0:
                self.rect.x += enemis_speed * -(rastoyanie_x / abs(rastoyanie_x))
        else:
            self.kill()
            self.live = False
        if self.rect.collidelistall(proj):
            self.heals -= damage
        if self.rect.colliderect(player.rect):
            player.heals -= self.damage
            if player.heals <= 0:
                player.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, go_x, go_y):
        super().__init__(proj_group)
        self.live = True
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.x = go_x
        self.y = go_y
        self.speed = [0, 0]
        self.rastoyanie_x = self.rect.x - self.x
        self.rastoyanie_y = self.rect.y - self.y
        if self.rastoyanie_y != 0 and self.rastoyanie_x != 0:
            if abs(self.rastoyanie_x) > abs(self.rastoyanie_y):
                koef = abs(self.rastoyanie_x) / abs(self.rastoyanie_y)
                self.speed = (5 * -(self.rastoyanie_x / abs(self.rastoyanie_x)),
                              5 * -(self.rastoyanie_y / abs(self.rastoyanie_y)) / koef)
            elif abs(self.rastoyanie_x) < abs(self.rastoyanie_y):
                koef = abs(self.rastoyanie_y) / abs(self.rastoyanie_x)
                self.speed = (5 * -(self.rastoyanie_x / abs(self.rastoyanie_x)) / koef,
                              5 * -(self.rastoyanie_y / abs(self.rastoyanie_y)))
            else:
                self.speed = (5 * -(self.rastoyanie_x / abs(self.rastoyanie_x)),
                              5 * -(self.rastoyanie_y / abs(self.rastoyanie_y)))
        elif self.rastoyanie_x == 0 and self.rastoyanie_y != 0:
            self.speed[1] = 5 * -(self.rastoyanie_y / abs(self.rastoyanie_y))
        elif self.rastoyanie_y == 0 and self.rastoyanie_x != 0:
            self.speed[0] = 5 * -(self.rastoyanie_x / abs(self.rastoyanie_x))

    def go(self):
        self.rect = self.rect.move(self.speed[0], self.speed[1])
        if self.rect.x > 500 or self.rect.x < 0 or self.rect.y > 850 or self.rect.y < 0:
            self.kill()
            self.live = False
        if self.rect.collidelistall(enemis):
            self.kill()
            self.live = False



def generate(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y, 0)
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.x < -obj.rect.width:
            obj.rect.x += (level_x + 1) * obj.rect.width
        if obj.rect.x >= obj.rect.width * level_x:
            obj.rect.x -= (level_x + 1) * obj.rect.width
        obj.rect.y += self.dy
        if obj.rect.y < -obj.rect.width:
            obj.rect.y += (level_y + 1) * obj.rect.width
        if obj.rect.y >= obj.rect.width * level_y:
            obj.rect.y -= (level_y + 1) * obj.rect.width

    def update(self, target):
        self.dx = w // 2 - (target.rect.x + target.rect.w // 2)
        self.dy = h // 2 - (target.rect.y + target.rect.h // 2)


#игровой цикл
def play():
    global all_sprites, enemi_group, tiles_group, player_group, box_g, player, \
        level_x, level_y, player_image, proj_group, proj
    pygame.mixer.music.load("data/gameplay_music.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    back_to_menu_button = Button(50, 50)
    camera = Camera()
    proj = []
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    proj_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemi_group = pygame.sprite.Group()
    box_g = pygame.sprite.Group()
    player = None
    player, level_x, level_y = generate(load_level(name))
    running = True
    goup = godown = goleft = goright = False
    icon = load_image("menu_btn.png")
    rect = icon.get_rect()
    while running:
        global spavnpoint
        spavnpoint += 1
        if spavnpoint % 300 == 0:
            enemis.append(Cube(0))
        for i in enemis:
            i.mislitelniy_process()
            if i.live == False:
                enemis.remove(i)
        for j in proj:
            j.go()
            if j.live == False:
                proj.remove(j)
        for event in pygame.event.get():
            back_to_menu_button.draw(450, 0, "menu", "menu")
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu()
                if event.key == pygame.K_m:
                    end_game()
                if event.key == pygame.K_LEFT:
                    goleft = True
                if event.key == pygame.K_RIGHT:
                    goright = True
                if event.key == pygame.K_UP:
                    goup = True
                if event.key == pygame.K_DOWN:
                    godown = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    goleft = False
                if event.key == pygame.K_RIGHT:
                    goright = False
                if event.key == pygame.K_UP:
                    goup = False
                if event.key == pygame.K_DOWN:
                    godown = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    bullet = Bullet(235, 410, pos[0], pos[1])
                    proj.append(bullet)

        if godown:
            player.rect.y += 2
        if goup:
            player.rect.y -= 2
        if goleft:
            player.rect.x -= 2
        if goright:
            player.rect.x += 2
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemi_group.draw(screen)
        proj_group.draw(screen)
        move_icon = rect.move(450, 0)
        screen.blit(icon, move_icon)
        pygame.display.flip()
        clock.tick(FPS)


show_menu()