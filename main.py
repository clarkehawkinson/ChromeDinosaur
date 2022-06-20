import pygame
import os
import random

pygame.init()

#Global Constants
screen_height = 600
screen_width = 1100
screen = pygame.display.set_mode((screen_width,screen_height))
Running = [pygame.image.load(os.path.join("Assets/Dino","DinoRun1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

Jumping = pygame.image.load(os.path.join("Assets/Dino","DinoJump.png"))

Ducking =  [pygame.image.load(os.path.join("Assets/Dino","DinoDuck1.png")),
    pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

Large_Cactus = [pygame.image.load(os.path.join("Assets/Cactus","LargeCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

Small_Cactus = [pygame.image.load(os.path.join("Assets/Cactus","SmallCactus1.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
    pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird","Bird1.png")),
    pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

Clouds = pygame.image.load(os.path.join("Assets/Other","Cloud.png"))

Track = pygame.image.load(os.path.join("Assets/Other","Track.png"))

class Dinosaur:
    #Top Left corner of picture
    x_pos = 80
    y_pos = 310
    y_pos_duck = 340
    jump_velo = 8.5

    def __init__(self):
        self.duck_img = Ducking
        self.run_img = Running
        self.jump_img = Jumping

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.jump_velo
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >=10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index //5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos_duck
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index //5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.x_pos
        self.dino_rect.y = self.y_pos
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel *4
            self.jump_vel -= .8
        if self.jump_vel < - self.jump_velo:
            self.dino_jump = False
            self.jump_vel = self.jump_velo

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = screen_width+random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = Clouds
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x <-self.width:
            self.x = screen_width + random.randint(2000, 3000)
            self.y = random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = screen_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, screen):
        if self.index >=9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index +=1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf',20)
    obstacles = []

    def score():
        global points, game_speed
        points +=.1
        if points % 10 == 0:
            game_speed += 1

        text = font.render('Points: ' + str(round(points,1)), True, (0,0,0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        screen.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = Track.get_width()
        screen.blit(Track, (x_pos_bg, y_pos_bg))
        screen.blit(Track, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(Track, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255,255,255))
        userInput = pygame.key.get_pressed()

        player.draw(screen)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(SmallCactus(Small_Cactus))
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(Large_Cactus))
            elif random.randint(0,2) == 2:
                obstacles.append(Bird(BIRD))
        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.draw.rect(screen, (255, 0, 0), player.dino_rect, 2)

        cloud.draw(screen)
        cloud.update()

        background()
        score()

        clock.tick(30)
        pygame.display.update()



main()
