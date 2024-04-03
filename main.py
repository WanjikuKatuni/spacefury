import pygame
# find path to imported images
import os
# font
pygame.font.init()
#  sound
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cool Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 200, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# create new event for when bullet hits the character. +1 & +2 are unique event IDs
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# spaceship image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# space background
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0,0)) #add image on screen
    pygame.draw.rect(WIN, BLACK, BORDER)   #draw border

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))   #draw the texts
    WIN.blit(yellow_health_text, (10, 10))


    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) #draw surface onto the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y)) 


    
    # draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):  #keys pressed list and yellow character
    if keys_pressed[pygame.K_a] and yellow.x - VEL - 20 > 0 : #left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):  #keys pressed list and yellow character
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red): #move bullets, handle collision of bullets with character and handle bullets when they collide with character 
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL #move bullets to the right
        if red.colliderect(bullet): #check if bullet collided with rect/yellow character
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH: #remove bullet when its past the width
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL #move bullets to the right
        if yellow.colliderect(bullet): #check if bullet collided with rect/yellow character
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0: #remove bullet when its past the width
            red_bullets.remove(bullet)


def draw_winner(text, red_health, yellow_health):
    WIN.blit(SPACE, (0,0)) #add image on screen
    pygame.draw.rect(WIN, BLACK, BORDER)   #draw border

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() -10, 10))   #draw the texts
    WIN.blit(yellow_health_text, (10, 10))
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) #pause for 5 seconnds to display winner before next game starts




# main game event loop
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) #never go under the capped fps for devices that went lower
        for event in pygame.event.get():  #checks for list of events and loops through them
            if event.type == pygame.QUIT: #check if use quits the window
                run = False
                pygame.quit()


            # bullets
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 -2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 -2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # events on hit
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # check if health is equal to zero to determine winnder
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins! "
        if winner_text != "":
            draw_winner(winner_text,  red_health,  yellow_health)
            break
#red.x += 1
        # print(red_bullets, yellow_bullets)
        keys_pressed = pygame.key.get_pressed() #tell what keys are currently being pressed
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
      
        handle_bullets(yellow_bullets, red_bullets, yellow, red) # check if the bullets colide with the characters

        #red.x += 1
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit() #closes pygame completely

    # restart the game
    main()

if __name__ == "__main__":
    main()