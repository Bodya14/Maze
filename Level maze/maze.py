import pygame
from levels import *
from time import time

pygame.init()

win_width, win_height = 700, 500
level_width = 860
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Догонялки")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

FPS = 60
clock = pygame.time.Clock()

pygame.mixer_music.load("jungles.ogg")
pygame.mixer_music.set_volume(0.2)
pygame.mixer_music.play(-1)

back = pygame.image.load("background.jpg")
back = pygame.transform.scale(back, (win_width, win_height))

class Camera:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed
    def move(self, player):
        if self.rect.right < level_width:
            if player.rect.x > self.rect.x + int(0.7*self.rect.w):
                self.rect.x += self.speed

camera = Camera(0, 0, win_width, win_height, 5)

class GameSprite:
    def __init__(self, x, y, w, h, image):
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
    def update(self):
        window.blit(self.image, (self.rect.x - camera.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image)
        self.speed = speed
    def move(self, down, up, left, right):
        k = pygame.key.get_pressed()
        if k[down]:
            if self.rect.bottom <= win_height:
                self.rect.y += self.speed
        if k[up]:
            if self.rect.y >= 0:
                self.rect.y -= self.speed
        if k[right]:
            if self.rect.x <= level_width - self.rect.width:
                self.rect.x += self.speed
        if k[left]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def collide(self, obj):
        if self.rect.colliderect(obj.rect):
            return True
        else:
            return False
bots = []
class Bot(GameSprite):
    def __init__(self, x, y, w, h, image, speed, x_finish):
        super().__init__(x, y, w, h, image)
        self.speed = speed
        if x > x_finish:
            self.direction = "left"
            self.x_start = x_finish
            self.x_finish = x
        else:
            self.direction = "right"
            self.x_start = x
            self.x_finish = x_finish
        bots.append(self)

    def move(self):
        if self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < self.x_start:
                self.direction = "right"
        elif self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x >+ self.x_finish:
                self.direction = "left"

player_img = pygame.image.load("hero.png")
player1 = Player(25, 25, 25, 25, player_img, 2)

bot_img = pygame.image.load("cyborg.png")
bot1 = Bot(220, 250, 25, 25, bot_img, 2.5, 280)
bot2 = Bot(55, 350, 25, 25, bot_img, 4, 160)

apple_img = pygame.image.load("apple.png")
banana_img = pygame.image.load("banana.png")
lemon_img = pygame.image.load("lemon.png")

block_img = pygame.image.load("block.png")

blocks = []
fruits = []
block_size = 20
x, y = 0, 0

for stroka in map1:
    for bl in stroka:
        if bl == "1":
            block = GameSprite(x, y, block_size, block_size, block_img)
            blocks.append(block)
        if bl == "2":
            apple = GameSprite(x, y, block_size, block_size, apple_img)
            fruits.append(apple)
        if bl == "3":
            banana = GameSprite(x, y, block_size, block_size, banana_img)
            fruits.append(banana)
        if bl == "4":
            lemon = GameSprite(x, y, block_size, block_size, lemon_img)
            fruits.append(lemon)
        x += block_size
    x = 0
    y += block_size
gold_img = pygame.image.load("treasure.png")
gold = GameSprite(650, 450, block_size, block_size, gold_img)

font = pygame.font.SysFont("Arial", 30)
font1 = pygame.font.SysFont("Arial", 20)
new_game_lb = font1.render("Щоб розпочати гру знову натисніть ПРОБІЛ", True, (20, 20, 20))

points = 0

game = True
finish = False
start_time = time()

while game:
    if not finish:
        camera.move(player1)
        game_time = int(time() - start_time)
        time_lb = font1.render('Час:' + str(game_time), True, (250, 250, 250))
        window.blit(back, (0, 0))
        player1.update()
        player1.move(pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT)
        gold.update()
        bot1.update()
        bot2.update()

        for bot in bots:
            bot.update()
            bot.move()
            if player1.collide(bot):
                game_over = font.render("Game Over!", True, (20, 20, 20))
                finish = True
        for fruit in fruits:
            fruit.update()
            if player1.collide(fruit):
                fruits.remove(fruit)
                points += 1

        for block in blocks:
            block.update()
            window.blit(time_lb, (0, 0))
            if player1.collide(block):
                game_over = font.render("Game Over!", True, (20, 20, 20))
                finish = True

        if player1.collide(gold):
            game_over = font.render("You Win!", True, (20, 20, 20))
            finish = True
    else:
        window.fill((255, 0, 0))
        window.blit(game_over, (250, 200))
        window.blit(new_game_lb, (150, win_height - 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and finish:
            finish = False
            player1 = Player(25, 25, 25, 25, player_img, 2)
            start_time = time()
            points = 0
            fruits = []
            x,y = 0,0
            for stroka in map1:
                for bl in stroka:
                    if bl == "2":
                        apple = GameSprite(x, y, block_size, block_size, apple_img)
                        fruits.append(apple)
                    if bl == "3":
                        banana = GameSprite(x, y, block_size, block_size, banana_img)
                        fruits.append(banana)
                    if bl == "4":
                        lemon = GameSprite(x, y, block_size, block_size, lemon_img)
                        fruits.append(lemon)
                    x += block_size
                x = 0
                y += block_size
    pygame.display.update()
    clock.tick(FPS)
