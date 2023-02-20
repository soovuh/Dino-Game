import pygame
from random import randint
from sys import exit


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(
        str(f'Score: {current_time}'), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [
            obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


# init pygame process
pygame.init()
# creating screen
screen = pygame.display.set_mode((800, 400))
# adding caption
pygame.display.set_caption('Dino-Game')
# creating clock obj
clock = pygame.time.Clock()

game_active = False
start_time = 0
score = 0
# creating text
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# creating surface background
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# obstacles
# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# creating player
player_walk_1 = pygame.image.load(
    'graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    'graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load(
    'graphics/player/jump.png').convert_alpha()
player_sit = pygame.image.load(
    'graphics/player/sit.png').convert_alpha()
player_sit_rect = player_sit.get_rect(midbottom=(60, 300))
sit = False

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(60, 300))
player_gravity = 0

# menu
player_stand_surf = pygame.transform.scale2x(pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha())
player_stand_rect = player_stand_surf.get_rect(center=(400, 200))

instruction_surf = test_font.render(
    'To start game click on Space', False, (64, 64, 64))
instruction_rect = instruction_surf.get_rect(center=(400, 325))

game_name_surf = test_font.render('Dino Game', False, (64, 64, 64))
game_name_rect = game_name_surf.get_rect(center=(400, 75))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    # close check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(
                        midbottom=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(
                        midbottom=(randint(900, 1100), 220)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

            # mouse controll
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            # keyboard space controll
            if event.type == pygame.KEYDOWN:
                if player_rect.bottom >= 300 and event.key in [pygame.K_SPACE, pygame.K_UP]:
                    player_gravity = -20
                if event.key == pygame.K_DOWN and player_rect.bottom >= 300:
                    sit = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN and player_rect.bottom == 300:
                    sit = False

            # restart check
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = pygame.time.get_ticks()

    # game part
    if game_active:
        # draw all our elements
        screen.blit(ground_surf, (0, 300))
        screen.blit(sky_surf, (0, 0))
        score = display_score()

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        if sit:
            screen.blit(player_sit, player_sit_rect)
            game_active = collisions(player_sit_rect, obstacle_rect_list)
        else:
            player_animation()
            screen.blit(player_surf, player_rect)
            game_active = collisions(player_rect, obstacle_rect_list)
        # obstacle
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    # restart part
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_name_surf, game_name_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (60, 300)
        player_gravity = 0
        sit = False

        score_message = test_font.render(
            f'Score: {score}', False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(400, 325))

        if score == 0:
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # update everything
    pygame.display.update()
    clock.tick(60)
