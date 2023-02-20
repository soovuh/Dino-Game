import pygame
from random import randint, choice
from sys import exit


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load(
            'graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load(
            'graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = - 20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200
        else:
            snail_1 = pygame.image.load(
                'graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load(
                'graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(
        str(f'Score: {current_time}'), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


# init pygame process, creating screen and adding caption
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Dino-Game')

# create score and clock
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# create font
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# initi player class and obstacle group
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# create surface background
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# create menu
player_stand_surf_1 = pygame.transform.scale2x(pygame.image.load(
    'graphics/player/player_stand.png').convert_alpha())
player_stand_rect_1 = player_stand_surf_1.get_rect(center=(400, 200))

player_stand_surf_2 = pygame.transform.scale2x(pygame.image.load(
    'graphics/player/player_stand2.png').convert_alpha())
player_stand_rect_2 = player_stand_surf_2.get_rect(center=(400, 200))

instruction_surf = test_font.render(
    'To start game click on Space', False, (64, 64, 64))
instruction_rect = instruction_surf.get_rect(center=(400, 325))

game_name_surf = test_font.render('Dino Game', False, (64, 64, 64))
game_name_rect = game_name_surf.get_rect(center=(400, 75))

# create timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

menu_sound = pygame.mixer.Sound('audio/menu.mp3')
menu_sound.set_volume(0.5)
menu_playing = True
# game process
while True:
    # close check
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    # game part
    if game_active:
        if menu_playing:
            menu_sound.stop()
            menu_playing = False
        # draw all our elements and call update() methods
        screen.blit(ground_surf, (0, 300))
        screen.blit(sky_surf, (0, 0))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # check on collision
        game_active = collision_sprite()

    # restart part
    else:
        if not menu_playing:
            menu_sound.play()
            menu_playing = True
        screen.fill((94, 129, 162))

        score_message = test_font.render(
            f'Score: {score}', False, (64, 64, 64))
        score_message_rect = score_message.get_rect(center=(400, 325))

        if score == 0:
            screen.blit(player_stand_surf_1, player_stand_rect_1)
            screen.blit(game_name_surf, game_name_rect)
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(player_stand_surf_2, player_stand_rect_2)
            screen.blit(game_name_surf, game_name_rect)
            screen.blit(score_message, score_message_rect)

    # update everything
    pygame.display.update()
    clock.tick(60)
