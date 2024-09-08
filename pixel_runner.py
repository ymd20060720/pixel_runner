# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 12:30:10 2024

@author: rikuto.yamada
"""

import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300
        
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
          
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300
            
        self.type = type
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
    
        
    def animation_state(self):
        self.index += 0.1
        if self.index >= len(self.frames):self.index = 0
        self.image = self.frames[int(self.index)]
        
    def movement(self):
        if self.type == 'fly':
            self.rect.x -= 8
        else:
            self.rect.x -= 6
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

        
    def update(self):
        self.animation_state()
        self.movement()
        self.destroy()
        
def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    print(current_time)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        updated_obstacles = []
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5  # assuming obstacle_rect is a pygame.Rect
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
            updated_obstacles.append(obstacle_rect)
        updated_obstacles = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return updated_obstacles
    else:
        return []
    
def collisions(player, obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    #play walking animation if player is on floor
    #display the jump surface when player is not on floor
    global player_surf, player_index
    
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]
    
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50) #font type, font size
game_active = False
start_time = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

#obstacles
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_index = 0
snail_surf = snail_frames[snail_index]

fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_index = 0
fly_surf = fly_frames[fly_index]

obstacle_rect_list = []

#player
player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

#intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2) #surface, angle, scale
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = test_font.render('Pixel Runner', False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('Press space to run', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.3)
bg_music.play(loops = -1)

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,400)
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.MOUSEMOTION and player_rect.bottom >= 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)
                
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surf = snail_frames[snail_index]
                
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surf = fly_frames[fly_index]
                    
                    
                
            
                
    if game_active:
        #screen.blit(test_surface,(0,350)) #structure,(coordinate)
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        #obstacle_movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        game_active = collision_sprite()
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: print('jump')
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        score_message = test_font.render(f'Your score: {score}', False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
    
    pygame.display.update()
    clock.tick(60)