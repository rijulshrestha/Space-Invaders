import pygame
import random
import math
from pygame import mixer
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('./static/background.png')

mixer.music.load("./static/background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invader")
icon = pygame.image.load('./static/rocket.png')
pygame.display.set_icon(icon)

# Player
player_image = pygame.image.load('./static/player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 6

speed_factor = 4

for i in range(number_of_enemies):
    enemy_image.append(pygame.image.load('./static/enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(speed_factor)
    enemy_y_change.append(30)

# Bullet

bullet_image = pygame.image.load('./static/bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_image, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))

def if_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

check = 0    

# Game Loop

running = True
while running:

    screen.fill((0, 0, 0))
    
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player_x_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("./static/laser.wav")
                    bulletSound.play()
                    
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player_x_change = 0

    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_enemies):

        if enemy_y[i] > 440:
            for j in range(number_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = speed_factor
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -speed_factor
            enemy_y[i] += enemy_y_change[i]

        collision = if_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosionSound = mixer.Sound("./static/explosion.wav")
            explosionSound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

            check += 1
            if check == 6 and speed_factor < 7:
                speed_factor += 0.5
                check = 0 

        enemy(enemy_x[i], enemy_y[i], i)

    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(textX, testY)
    pygame.display.update()
