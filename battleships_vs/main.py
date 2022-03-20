import pygame
import os
import sys

pygame.init()
dir_path = os.path.dirname(os.path.realpath(__file__))

#Colors
ORANGE  = (255, 140, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 255, 0)
LIGHT = (170, 170, 170)
DARK = (0, 0, 0)

#Window
WIDTH, HEIGHT = 1024, 680
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
FPS = 60
VEL = 5
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
START_SCREEN = pygame.transform.scale(pygame.image.load(os.path.join(dir_path, 'Assets', 'start-screen.jpg')), (WIDTH, HEIGHT))
pygame.display.set_caption("Battleships")
SPACE = pygame.transform.scale(pygame.image.load(os.path.join(dir_path, 'Assets', 'water.jpg')), (WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

#Figures
BATTLESHIP_WIDTH, BATTLESHIP_HEIGTH = 80, 60
YELLOW_BATTLESHIP_IMG = pygame.image.load(os.path.join(dir_path, 'Assets', 'battleship_yellow.png'))
YELLOW_BATTLESHIP = pygame.transform.scale(YELLOW_BATTLESHIP_IMG, (BATTLESHIP_WIDTH, BATTLESHIP_HEIGTH))
RED_BATTLESHIP_IMG = pygame.image.load(os.path.join(dir_path, 'Assets', 'battleship_red.png'))
RED_BATTLESHIP = pygame.transform.scale(RED_BATTLESHIP_IMG, (BATTLESHIP_WIDTH, BATTLESHIP_HEIGTH))
SHIP_SOUND = pygame.mixer.Sound(os.path.join(dir_path, 'Assets', 'boat_sound.mp3'))


#Bullets
BULLET_VEL = 10
MAX_BULLETS = 3
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join(dir_path, 'Assets', 'Grenade.mp3'))
BULLET_SHOT_SOUND = pygame.mixer.Sound(os.path.join(dir_path, 'Assets', 'Gun.mp3'))

#Clock Setting
clock = pygame.time.Clock()

def draw_window(red, yellow , red_bullet, yellow_bullet, red_health, yellow_health):
    SCREEN.blit(SPACE, (0, 0))
    pygame.draw.rect(SCREEN, BLACK, BORDER)
    SCREEN.blit(RED_BATTLESHIP, (red.x, red.y))
    SCREEN.blit(YELLOW_BATTLESHIP, (yellow.x, yellow.y))

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    SCREEN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    SCREEN.blit(yellow_health_text, (10, 10))

    for bullet in red_bullet:
        pygame.draw.rect(SCREEN, RED, bullet)

    for bullet in yellow_bullet:
        pygame.draw.rect(SCREEN, YELLOW, bullet)

    pygame.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
    
def yellow_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: #left
        red.x -= VEL 
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x: #right
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y + VEL > 0: #up
        red.y -= VEL 
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT: #down
        red.y += VEL

def red_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x + VEL > BORDER.x: #Left
        yellow.x -= VEL 
    if keys_pressed[pygame.K_RIGHT] and yellow.x + BATTLESHIP_WIDTH < WIDTH: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y + VEL > 0: #up
        yellow.y -= VEL 
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT: #down
        yellow.y += VEL

def handle_bullets(red_bullet, yellow_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL

        if bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)

    for bullet in red_bullet:
        bullet.x -= BULLET_VEL

        if bullet.x < 0:
            red_bullet.remove(bullet)
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)





def start_menu():
    smallfont = pygame.font.SysFont('Corbel',35)
    title_text = smallfont.render('BATTLESHIPS' , True , DARK)
    start_text = smallfont.render('START' , True , DARK)
    quit_text = smallfont.render('QUIT' , True , DARK)
    #SHIP_SOUND.play()

    while True:
        
        for event in pygame.event.get():
            #QUIT
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #Start Game
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 550 <= mouse[0] <= 700 and 280 <= mouse[1] <= 315:
                    game()

                if 550 <= mouse[0] <= 700 and 350 <= mouse[1] <= 380:
                    pygame.quit()
                    sys.exit()
            

        SCREEN.blit(START_SCREEN, (0, 0))
        #pygame.draw.rect(SCREEN, DARK, [500, 275, 200, 50])
        SCREEN.blit(title_text , (550, 100))
        SCREEN.blit(start_text , (550, 280))
        SCREEN.blit(quit_text , (550, 350))
        pygame.display.update()
        clock.tick(60)
        return True


def game():
    yellow = pygame.Rect(100, 300, BATTLESHIP_WIDTH, BATTLESHIP_HEIGTH)
    red = pygame.Rect(700, 300, BATTLESHIP_WIDTH, BATTLESHIP_HEIGTH)

    red_bullet = []
    yellow_bullet = []
    red_health = 10
    yellow_health = 10

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     

            if event.type == pygame.KEYDOWN and len(red_bullet) < MAX_BULLETS:
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_SHOT_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullet.append(bullet)
                    BULLET_SHOT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            return False

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)      
        handle_bullets(red_bullet, yellow_bullet, yellow, red)
        draw_window(red, yellow, red_bullet, yellow_bullet, red_health, yellow_health)
        clock.tick(60)


if __name__ == "__main__":
    while True:
        start_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(15)