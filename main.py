import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('Backgrounds/space.jpg')

# Play Button
play_button = pygame.draw.rect(screen, (0, 0, 240), (150, 90, 100, 50))

# Background sound
mixer.music.load('Sounds/background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Wars")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('Spaceships/player3.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
enemyX_change = []
number_of_enemies = 6
for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0.4
bulletY_change = 1.8
bullet_state = "ready"  # Ready state means you can't the see the bullet
# fire state means bullet is moving

# Score
score_value = 0

# High score
with open('highscore.txt', 'r') as file:
    k = file.read()
high_score = int(k)
High_score = pygame.font.Font('freesansbold.ttf', 20)


font = pygame.font.Font('freesansbold.ttf', 20)
textX, textY = 10, 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 60)
start = pygame.font.Font('freesansbold.ttf', 80)
# Exit = pygame.font.Font('freesansbold.ttf', 32)
play = pygame.font.Font('freesansbold.ttf', 32)



def startMenu():
    screen.blit(background, (0, 0))


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_high_score(x, y):
    global high_score
    Highscore = High_score.render("High Score: " + str(high_score), True, (255, 255, 255))
    screen.blit(Highscore, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (250, 250, 20))
    screen.blit(over_text, (220, 250))
    with open('highscore.txt', 'w') as f:
        f.write(str(high_score))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(eX, eY, bX, bY):
    distance = math.sqrt(math.pow(bX - eX, 2) + math.pow(bY - eY, 2))
    if distance < 27:
        return True
    return False


def main():
    global playerX, playerY, playerX_change, playerY_change, bulletX, bulletY, bullet_state, score_value, high_score
    running = True
    while running:
        # setting background color (RGB)
        startMenu()
        screen.fill((0, 0, 30))
        # Background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if score_value > high_score:
                    high_score = score_value
                    with open('highscore.txt', 'w') as fl:
                        fl.write(str(high_score))
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.45
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 0.45
                elif event.key == pygame.K_UP:
                    playerY_change = -0.45
                elif event.key == pygame.K_DOWN:
                    playerY_change = 0.45
                if event.key == pygame.K_SPACE and bullet_state == 'ready':
                    bullet_sound = mixer.Sound('Sounds/laser.wav')
                    bullet_sound.play()
                    # Get the current x coordinate of the space ship
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        # Checking for boundaries of spaceship so it doesn't go out of bounds
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy movement
        for i in range(number_of_enemies):
            # Game over
            if enemyY[i] > 440:
                for j in range(number_of_enemies):
                    enemyY[i] = 3000
                if score_value > high_score:
                    high_score = score_value
                game_over_text()
                break
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.4
                enemyY[i] += enemyY_change[i]

                # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

            if collision:
                explosion_Sound = mixer.Sound('Sounds/explosion.wav')
                explosion_Sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            enemy(enemyX[i], enemyY[i], i)

        # Bullet movement
        if bulletY <= -30:
            bulletY = 480
            bullet_state = 'ready'
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        playerY += playerY_change
        player(playerX, playerY)
        show_score(textX, textY)
        show_high_score(640, 10)

        pygame.display.update()


# Game loop


flag = True
while flag:
    startMenu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (345, 300) <= pygame.mouse.get_pos() <= (445, 340):
                main()
                flag = False

            if (345, 370) <= pygame.mouse.get_pos() <= (445, 410):
                flag = False

    Game = start.render("Space Wars", True, (0, 100, 255))
    screen.blit(Game, (170, 200))
    start_button = pygame.draw.rect(screen, (0, 150, 240), (345, 300, 100, 40))
    play_button = play.render('Play', True, (0, 0, 0))
    screen.blit(play_button, (360, 305))

    pygame.display.update()
