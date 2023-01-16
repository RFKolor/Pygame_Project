import pygame
import os
import sys
import random
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

name = 'level1.txt'
char_name = 'midas'

pygame.init()
size = w, h = 500, 840
pygame.display.set_caption("Reverenge Georgis")
FPS = 60
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
# пока босс жив переменна true, когда босс повержен переменная меняется на false,используется для
# экрана окончания
spavnpoint = 0
enemis = []
enemis_speed = 1
damage = 5
music_volume = 0.5
# костыль чтобы слайдер корректно работал
slider = Slider(screen, 25, 200, 300, 20, min=0, max=100, step=1, colour=(76, 81, 74),
                handleColour=(255, 255, 255))
show_boss_hp_bar = False
#количество очков заработанных за 1 забаег
point = 0
cube_point = 1
zombie_point = 1
dragon_point = 1
animator = 0
mnoj_hp_cube = 0.1
mnoj_dmg_cube = 0.1
mnoj_spavnrate_cube = 1.5
heals_cube = 1
damage_cube = 1
spavnrate_cube = 200
mnoj_hp_zombie = 1
mnoj_dmg_zombie = 1
mnoj_spavnrate_zombie = 1
heals_zombie = 10
damage_zombie = 3
spavnrate_zombie = 150
mnoj_hp_dragon = 5
mnoj_dmg_dragon = 1
mnoj_spavnrate_dragon = 2
heals_dragon = 100
damage_dragon = 25
spavnrate_dragon = 500
boss = False
eggs = []
georg = []


class Button:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.button_click = pygame.mixer.Sound("data/button.wav")

    def draw(self, x, y, text, function=None):
        # function передает вызов функции или саму функцию,допустим начало игры или выход
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, (76, 81, 74), (x, y, self.width, self.height), 0)
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
                        elif function == "settings":
                            settings()


# функция для печатания текста
def print_text(text, x, y, font_color=(0, 0, 0), font_size=50):
    font_type = pygame.font.SysFont('arial', font_size)
    message = font_type.render(text, True, font_color)
    screen.blit(message, (x, y))


# настройки игры(звук)
def settings():
    global music_volume
    image_background = pygame.image.load("data/menu_bg.png").convert_alpha()
    show = True
    accept_btn = Button(150, 70)
    # заготовка, в дальнейшем,если возможно будет возможность выбора трека в меню и в самой игре
    music_btn = Button(125, 70)
    help_btn = Button(25, 70)
    while show:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            screen.blit(image_background, (0, 0))
            accept_btn.draw(175, 680, "Accept", "menu")
            # изменение громкости музыки
            print_text(f"volume of music {slider.getValue()}%", 25, 230, (166, 189, 215), 30)
            print_text("Settings", 150, 0, (90, 0, 0), 70)
            print_text("Volume", 180, 120, (166, 189, 215), 50)

            music_volume = slider.getValue() * 0.01
            pygame_widgets.update(events)
            pygame.display.update()
    pygame.display.flip()


# главное меню
def show_menu():
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    image_background = pygame.image.load("data/menu_bg.png").convert_alpha()
    show = True
    start_game_button = Button(230, 70)
    quit_game_button = Button(100, 70)
    setting_game_button = Button(150, 70)
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    play()
        screen.blit(image_background, (0, 0))
        print_text("Reverenge Georgis", 0, 0, (90, 0, 0), 70)
        print_text("Exclusive edition", 100, 90, (166, 189, 215), 50)
        start_game_button.draw(135, 255, "Start Game", "play")
        setting_game_button.draw(175, 425, "Setting", "settings")
        quit_game_button.draw(200, 595, "Quit", "exit")
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


def ng_plus():
    global mnoj_hp_dragon, mnoj_hp_zombie, mnoj_hp_cube, mnoj_dmg_zombie, mnoj_dmg_dragon, \
    mnoj_dmg_cube
    mnoj_dmg_dragon *= 2
    mnoj_dmg_cube *= 2
    mnoj_dmg_zombie *= 2
    mnoj_hp_cube *= 2
    mnoj_hp_zombie *= 2
    mnoj_hp_dragon *= 2


tile = load_image('ground.png')
cube_images = [load_image('enemis/cube.png'), load_image('enemis/cube1.png'),
               load_image('enemis/cube2.png'), load_image('enemis/cube3.png')]
zombie_images = [load_image('enemis/zombie.png'), load_image('enemis/zombie1-3.png'),
                 load_image('enemis/zombie2.png'), load_image('enemis/zombie1-3.png')]
dragon_images = [load_image('enemis/dragon.png'), load_image('enemis/dragon2.png'),
                 load_image('enemis/dragon3.png'), load_image('enemis/dragon4.png'),
                 load_image('enemis/dragon5.png'), load_image('enemis/dragon6.png')]
georg_images = [load_image('enemis/Georgis.png'), load_image('enemis/Georgis1.png'),
                load_image('enemis/Georgis2.png'), load_image('enemis/Georgis3.png'),
                load_image('enemis/Georgis4.png'), load_image('enemis/Georgis5.png'),
                load_image('enemis/Georgis6.png'), load_image('enemis/Georgis7.png')]
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


def itembar(key):
    pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == 'wall':
            self.add(box_g)
        self.image = tile
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x, tile_h * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.heals = 1000
        self.atakspeed = 25
        self.atak = 1
        self.speed = 2
        self.gold = 0
        self.image = player_images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x + 15, tile_h * pos_y + 5)

    def animate(self,frame):
        self.x = self.rect.x
        self.y = self.rect.y
        self.image = player_images[frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)


# меню окончания игры
def end_game():
    global point
    global music_volume
    global  eggs, enemis, proj, georg, cube_point, dragon_point, zombie_point, heals_zombie, \
    heals_dragon, heals_cube, damage_cube, damage_zombie, damage_dragon, spavnrate_zombie, \
    spavnrate_dragon, spavnrate_cube, boss, gt
    pygame.mixer.music.load("data/menu.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    image_background = pygame.image.load("data/menu_bg.png").convert_alpha()
    show = True
    start_game_button = Button(150, 70)
    quit_game_button = Button(100, 70)
    if not boss:
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
        print_text(f"Your score {player.gold}", 100, 383, (76, 81, 74), 70)
        start_game_button.draw(0, 775, "Restart", "play")
        global enemis, proj
        enemis = []
        proj = []
        eggs = []
        georg = []
        boss = gt = False
        cube_point = dragon_point = zombie_point = heals_zombie = heals_dragon = heals_cube = \
        damage_cube = damage_zombie = damage_dragon = spavnrate_zombie = spavnrate_dragon = \
        spavnrate_cube = 0
        quit_game_button.draw(400, 775, "Quit", "exit")
        pygame.display.flip()


class Georgis(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemi_group, all_sprites)
        global eggs
        self.heals = 10000
        self.live = True
        self.frame = 0
        self.damage = 100
        self.speed = 3
        self.image = georg_images[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(500, 0)

    def mislitelniy_process(self):
        global point
        if self.heals > 0:
            if self.rect.x < 0:
                self.rect.x = 0
            if self.rect.x > 500:
                self.rect.x = 500
            if self.rect.y < 0:
                self.rect.y = 0
            if self.rect.y > 840:
                self.rect.y = 840
            rastoyanie_x = self.rect.x - player.rect.x
            rastoyanie_y = self.rect.y - player.rect.y
            if rastoyanie_y != 0 and rastoyanie_x != 0:
                if abs(rastoyanie_x) > abs(rastoyanie_y):
                    koef = abs(rastoyanie_x) / abs(rastoyanie_y)
                    self.rect = self.rect.move(self.speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)),
                                               self.speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)) / koef)
                elif abs(rastoyanie_x) < abs(rastoyanie_y):
                    koef = abs(rastoyanie_y) / abs(rastoyanie_x)
                    self.rect = self.rect.move(self.speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)) / koef,
                                               self.speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)))
                else:
                    self.rect = self.rect.move(self.speed *
                                               -(rastoyanie_x / abs(rastoyanie_x)),
                                               self.speed *
                                               -(rastoyanie_y / abs(rastoyanie_y)))
            elif rastoyanie_x == 0 and rastoyanie_y != 0:
                self.rect.y += self.speed * -(rastoyanie_y / abs(rastoyanie_y))
            elif rastoyanie_y == 0 and rastoyanie_x != 0:
                self.rect.x += self.speed * -(rastoyanie_x / abs(rastoyanie_x))
        else:
            self.kill()
            self.live = False
            point += 1000
        if self.rect.collidelistall(proj):
            self.heals -= damage
        if self.rect.colliderect(player.rect):
            player.heals -= self.damage
            if player.heals <= 0:
                player.kill()
                end_game()

    def bomb_atak(self):
        for i in range(8):
            eggs.append(Egg(i))

    def charge(self):
        vay = random.choice((1, 2))
        self.orel = pygame.mixer.Sound("data/orel.mp3")
        pygame.mixer.Sound.play(self.orel)
        if vay == 1:
            self.rect = self.rect.move(random.randint(-600, 600), 0)
        else:
            self.rect = self.rect.move(0, random.randint(-600, 600))

    def animate(self):
        self.x = self.rect.x
        self.y = self.rect.y
        if self.frame == 6:
            self.frame = 0
        if self.rect.x - player.rect.x > 0:
            self.image = georg_images[self.frame]
            self.frame += 1
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)
        else:
            self.image = georg_images[self.frame]
            self.frame += 1
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)


class Egg(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__(enemi_group, all_sprites)
        self.damage = 333
        self.form = 0
        self.cloack = 0
        self.heals = 10
        self.live = True
        self.number = number
        self.bomb_damage = 1665
        self.image = load_image('enemis/egg.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(georg[0].rect.x + 135, georg[0].rect.y + 200)
        self.startpos = (self.rect.x, self.rect.y)

    def left(self):
        self.rect = self.rect.move(-6, 0)

    def up(self):
        self.rect = self.rect.move(0, -6)

    def right(self):
        self.rect = self.rect.move(6, 0)

    def down(self):
        self.rect = self.rect.move(0, 6)

    def left_down(self):
        self.rect = self.rect.move(-3, 3)

    def left_up(self):
        self.rect = self.rect.move(-3, -3)

    def right_up(self):
        self.rect = self.rect.move(3, -3)

    def right_down(self):
        self.rect = self.rect.move(3, 3)

    def hit(self):
        if self.form == 0:
            if self.rect.colliderect(player.rect):
                player.heals -= self.damage
                if player.heals <= 0:
                    player.kill()
                    end_game()
        else:
            if self.rect.colliderect(player.rect):
                player.heals -= self.bomb_damage
                if player.heals <= 0:
                    player.kill()
                    end_game()

    def Boom(self):
        if self.cloack == 100:
            self.form = 1
            self.x = self.rect.x
            self.y = self.rect.y
            self.image = load_image('enemis/boom.png')
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)
        self.cloack += 1

    def Live(self):
        if self.heals == 0:
            self.kill()
            self.live = False

    def animate(self):
        self.x = self.rect.x
        self.y = self.rect.y
        if self.number < 4:
            self.image = pygame.transform.rotate(self.image, 270)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)
        else:
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)


class Cube(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemi_group, all_sprites)
        self.live = True
        self.frame = 0
        self.gp = [10, 1]
        self.damage = damage_cube
        self.image = cube_images[0]
        self.rect = self.image.get_rect()
        self.heals = heals_cube
        if random.choice((0, 1)) == 1:
            self.rect = self.rect.move(random.choice((-25, 500)), random.randint(-25, 851))
        else:
            self.rect = self.rect.move(random.randint(-25, 500), random.choice((-25, 851)))

    def mislitelniy_process(self):
        global point, cube_point
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
            point += self.gp[1]
            player.gold += self.gp[0]
            if char_name == 'midas':
                player.gold += self.gp[0] * 20 // 100
            cube_point += 1
        if self.rect.collidelistall(proj):
            self.heals -= damage
        if self.rect.colliderect(player.rect):
            player.heals -= self.damage
            if player.heals <= 0:
                player.kill()
                end_game()

    def animate(self):
        self.x = self.rect.x
        self.y = self.rect.y
        if self.frame == 4:
            self.frame = 0
        self.image = cube_images[self.frame]
        self.frame += 1
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x, self.y)


class Zombie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemi_group, all_sprites)
        self.live = True
        self.frame = 0
        self.gp = [25, 5]
        self.damage = damage_zombie
        self.image = zombie_images[0]
        self.rect = self.image.get_rect()
        self.heals = heals_zombie
        if random.choice((0, 1)) == 1:
            self.rect = self.rect.move(random.choice((-25, 500)), random.randint(-25, 851))
        else:
            self.rect = self.rect.move(random.randint(-25, 500), random.choice((-25, 851)))

    def mislitelniy_process(self):
        global point, zombie_point
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
            point += self.gp[1]
            player.gold += self.gp[0]
            if char_name == 'midas':
                player.gold += self.gp[0] * 20 // 100
            zombie_point += 1
        if self.rect.collidelistall(proj):
            self.heals -= damage
        if self.rect.colliderect(player.rect):
            player.heals -= self.damage
            if player.heals <= 0:
                player.kill()
                end_game()

    def animate(self):
        self.x = self.rect.x
        self.y = self.rect.y
        if self.frame == 3:
            self.frame = 0
        if self.rect.x - player.rect.x > 0:
            self.image = zombie_images[self.frame]
            self.frame += 1
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)
        else:
            self.image = zombie_images[self.frame]
            self.frame += 1
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)


class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(enemi_group, all_sprites)
        self.live = True
        self.frame = 0
        self.gp = [100, 25]
        self.damage = damage_dragon
        self.image = dragon_images[0]
        self.rect = self.image.get_rect()
        self.heals = heals_dragon
        if random.choice((0, 1)) == 1:
            self.rect = self.rect.move(random.choice((-25, 500)), random.randint(-25, 851))
        else:
            self.rect = self.rect.move(random.randint(-25, 500), random.choice((-25, 851)))

    def mislitelniy_process(self):
        global point, dragon_point
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
            point += self.gp[1]
            player.gold += self.gp[0]
            if char_name == 'midas':
                player.gold += self.gp[0] * 20 // 100
            dragon_point += 1
        if self.rect.collidelistall(proj):
            self.heals -= damage
        if self.rect.colliderect(player.rect):
            player.heals -= self.damage
            if player.heals <= 0:
                player.kill()
                end_game()

    def animate(self):
        self.x = self.rect.x
        self.y = self.rect.y
        if self.frame == 5:
            self.frame = 0
        if self.rect.x - player.rect.x > 0:
            self.image = dragon_images[self.frame]
            self.frame += 1
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)
        else:
            self.image = dragon_images[self.frame]
            self.frame += 1
            self.rect = self.image.get_rect()
            self.rect = self.rect.move(self.x, self.y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, go_x, go_y):
        super().__init__(proj_group)
        self.live = True
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.heals = 2
        self.x = go_x
        self.y = go_y
        self.speed = [0, 0]
        self.attack_sound = pygame.mixer.Sound("data/range_attack.mp3")
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

    def sound(self):
        pygame.mixer.Sound.play(self.attack_sound)

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
                new_player = Player(x, y)
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


# игровой цикл
def play():
    global all_sprites, enemi_group, tiles_group, player_group, box_g, player, \
           level_x, level_y, player_image, proj_group, proj, heals_cube, damage_cube, \
           spavnrate_cube, animator, eggs, georg, cube_point, zombie_point, dragon_point, \
           heals_zombie, damage_zombie, spavnrate_zombie, heals_dragon, damage_dragon, \
           spavnrate_dragon, boss, georgis, show_boss_hp_bar
    pygame.mixer.music.load("data/gameplay_music.mp3")
    pygame.mixer.music.set_volume(music_volume)
    pygame.mixer.music.play(-1)
    back_to_menu_button = Button(50, 50)
    camera = Camera()
    proj = []
    oldpoint_cube = cube_point
    oldpoint_zombie = zombie_point
    oldpoint_dragon = dragon_point
    can_atak = 0
    frame_tick = 0
    spavnrate_cub = 200
    spavnrate_zomb = 150
    spavnrate_drag = 500
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    proj_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemi_group = pygame.sprite.Group()
    box_g = pygame.sprite.Group()
    player = None
    egg_rate = 0
    zombie_timer = 0
    dragon_timer = 0
    timer = 0
    gt = False
    player, level_x, level_y = generate(load_level(name))
    running = True
    goup = godown = goleft = goright = False
    icon = load_image("menu_btn.png")
    rect = icon.get_rect()
    max_health = player.heals * 0.1 + 10
    hp = player.heals * 0.1
    #иконка для денюжки
    gold_icon = load_image("gold.png")
    gold_icon = pygame.transform.scale(gold_icon, (25, 25))
    gold_rect = gold_icon.get_rect()
    #кнопки для item bar
    while running:
        global spavnpoint
        if animator == 4:
            animator = 0
        player.animate(animator)
        if frame_tick % 10 == 0:
            animator += 1
        if cube_point > oldpoint_cube:
            heals_cube += mnoj_hp_cube
            damage_cube += mnoj_dmg_cube
            spavnrate_cube -= mnoj_spavnrate_cube
            if spavnrate_cube < 1:
                spavnrate_cube = 1
            if spavnrate_cube % 1 != 0:
                spavnrate_cub = spavnrate_cube // 1
            oldpoint_cube = cube_point
        if zombie_point > oldpoint_zombie:
            heals_zombie += mnoj_hp_zombie
            damage_zombie += mnoj_dmg_zombie
            spavnrate_zombie -= mnoj_spavnrate_zombie
            if spavnrate_zombie < 1:
                spavnrate_zombie = 1
            if spavnrate_zombie % 1 != 0:
                spavnrate_zomb = spavnrate_zombie // 1
            oldpoint_zombie = zombie_point
        if dragon_point > oldpoint_dragon:
            heals_dragon += mnoj_hp_dragon
            damage_dragon += mnoj_dmg_dragon
            spavnrate_dragon -= mnoj_spavnrate_dragon
            if spavnrate_dragon < 1:
                spavnrate_dragon = 1
            if spavnrate_dragon % 1 != 0:
                spavnrate_drag = spavnrate_dragon // 1
            oldpoint_dragon = dragon_point
        spavnpoint += 1
        if not boss:
            if spavnpoint % spavnrate_cub == 0:
                enemis.append(Cube())
                if cube_point % 10 == 0:
                    enemis.append(Cube())
            zombie_timer += 1
            dragon_timer += 1
            if zombie_timer > 18000:
                if spavnpoint % spavnrate_zombie == 0:
                    enemis.append(Zombie())
                    if zombie_point % 5 == 0:
                        enemis.append(Zombie())
                        enemis.append(Zombie())
            if zombie_timer > 36000:
                if spavnpoint % spavnrate_dragon == 0:
                    enemis.append(Dragon())
                    if dragon_point % 10 == 0:
                        for i in range(5):
                            enemis.append(Dragon())
        if boss:
            show_boss_hp_bar = True
            if georg[0].live == False:
                end_game()
                boss = False
                gt = False
                ng_plus()
        can_atak += 1
        frame_tick += 1
        if can_atak % player.atakspeed == 0:
            player.atak = 1
        for i in enemis:
            i.mislitelniy_process()
            if frame_tick % 10 == 0:
                i.animate()
            if i.live == False:
                enemis.remove(i)
        for j in proj:
            j.go()
            if j.heals == 0:
                proj.remove(j)
            if j.live == False:
                j.heals -= 1
        egg_rate += 1
        if egg_rate % 54000 == 0:
            if not gt:
                roar = pygame.mixer.Sound("data/rev.wav")
                pygame.mixer.Sound.play(roar)
                georgis = Georgis()
                georg.append(georgis)
                enemis.append(georgis)
                boss = True
                gt = True
        if gt == True:
            if egg_rate % 100 == 0:
                georgis.bomb_atak()
            dash = random.randint(0, 300)
            if dash == 1:
                georgis.charge()
            for i in eggs:
                if i.number == 0:
                    if i.form == 0:
                        i.left()
                        i.Boom()
                elif i.number == 1:
                    if i.form == 0:
                        i.left_up()
                        i.Boom()
                elif i.number == 2:
                    if i.form == 0:
                        i.up()
                        i.Boom()
                elif i.number == 3:
                    if i.form == 0:
                        i.right_up()
                        i.Boom()
                elif i.number == 4:
                    if i.form == 0:
                        i.right()
                        i.Boom()
                elif i.number == 5:
                    if i.form == 0:
                        i.right_down()
                        i.Boom()
                elif i.number == 6:
                    if i.form == 0:
                        i.down()
                        i.Boom()
                elif i.number == 7:
                    if i.form == 0:
                        i.left_down()
                if egg_rate % 5 == 0:
                    i.animate()
                i.Boom()
                i.hit()
                i.Live()
                if i.form != 0:
                    i.heals -= 1
                if i.live == False:
                    eggs.remove(i)
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
                    if player.atak == 1:
                        pos = pygame.mouse.get_pos()
                        bullet = Bullet(235, 410, pos[0], pos[1])
                        proj.append(bullet)
                        bullet.sound()
                        player.atak = 0
                        can_atak = 0
        if godown:
            player.rect.y += player.speed
        if goup:
            player.rect.y -= player.speed
        if goleft:
            player.rect.x -= player.speed
        if goright:
            player.rect.x += player.speed
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemi_group.draw(screen)
        proj_group.draw(screen)
        # таймер
        time = f'{timer // 60 // 60}:{timer // 60 % 60}'
        font = pygame.font.SysFont('Consolas', 30)
        screen.blit(font.render(time, True, (0, 0, 0)), (245, 5))
        timer += 1
        #hp bar
        pygame.draw.rect(screen, (0, 0, 0), (5, 5, max_health, 40), 5)
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, player.heals * 0.1, 30))
        print_text(f"{round(player.heals * 0.1)}", hp / 2 - (5 * hp * 0.01), 12, (0, 0, 0), 20)
        #иконка выходы в меню(паузы)
        move_icon = rect.move(450, 0)
        screen.blit(icon, move_icon)
        #денюжки
        move_gold_icon = gold_rect.move(0, 50)
        print_text(f"{player.gold}", 25, 50, (255, 255, 255), 20)
        screen.blit(gold_icon, move_gold_icon)
        #hp bar boss
        if boss:
            pygame.draw.rect(screen, (255, 0, 0), (150, 100, georgis.heals * 0.02, 30))
            pygame.draw.rect(screen, (0, 0, 0), (150, 95, 10000 * 0.02, 40), 5)
            print_text(f"{round(georgis.heals * 0.1)}", 170, 100, (0, 0, 0), 30)
        pygame.display.flip()
        clock.tick(FPS)


show_menu()