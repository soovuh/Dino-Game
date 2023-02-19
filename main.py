import pygame
from sys import exit


# init pygame process
pygame.init()
# creating screen
screen = pygame.display.set_mode((800, 400))
# adding caption
pygame.display.set_caption('Dino-Game')
# creating clock obj
clock = pygame.time.Clock()

# creating font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# creating surface background
sky_surface = pygame.image.load('graphics/sky.png')
ground_surface = pygame.image.load('graphics/ground.png')
text_surface = test_font.render('Dino game', False, 'black')

# creating enemy
snail_surface = pygame.image.load('graphics/snail/snail1.png')
snail_x_pos = 600

while True:
    # close check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # draw all our elements
    screen.blit(ground_surface, (0, 300))
    screen.blit(sky_surface, (0, 0))
    screen.blit(text_surface, (350, 50))
    
    snail_x_pos -= 1
    screen.blit(snail_surface, (snail_x_pos, 270))
    if snail_x_pos == -80:
        snail_x_pos = 820
    # update everything
    pygame.display.update()
    clock.tick(60)
