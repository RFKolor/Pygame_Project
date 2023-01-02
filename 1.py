import pygame
import os
import sys

name = 'level1.txt'
char_name = 'chars/midas.png'

pygame.init()
size = w, h = 500, 500
game.display.set_caption("Reverenge Georgis")
FPS = 50
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


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


def show_menu():
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
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(tile_w * pos_x + 15, tile_h * pos_y + 5)


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


def play():
    global all_sprites, all_sprites, tiles_group, player_group, box_g
    back_to_menu_button = Button(50, 50)
    camera = Camera()
    all_sprites = pygame.sprite.Group()
    player_image = load_image(char_name)
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    box_g = pygame.sprite.Group()
    player = None
    player, level_x, level_y = generate(load_level(name))
    running = True
    goup = godown = goleft = goright = False
    icon = load_image("menu_btn.png")
    rect = icon.get_rect()
    while running:
        for event in pygame.event.get():
            back_to_menu_button.draw(450, 0, "menu", "back_to menu")
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
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
        move_icon = rect.move(450, 0)
        screen.blit(icon, move_icon)
        pygame.display.flip()
        clock.tick(FPS)

show_menu()
