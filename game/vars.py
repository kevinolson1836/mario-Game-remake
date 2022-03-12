from turtle import Screen
from matplotlib import scale
import pygame
from pygame.locals import *
import random
import time
import sys
import math
import bird
import background
import tank
import platforms
import instructions_screen
import movement
import sprite_sheet_class as ss



# basic vars and some pygame setup
pygame.init()
WINDOW_SIZE = (1400, 1000)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = list(screen.get_size())
frame_count = 0
fps = 30
start_loop = True
black = (0,0,0)
clock = pygame.time.Clock()
pygame.display.set_caption("Game")




# load sprites
bullet_image = pygame.image.load("img/bullet.png")
tank_image = pygame.image.load("img/tank.png")
boss_image = pygame.image.load("img/boss.png")
background1 = background.background('img/sewer.png', [0,0])
start_background = background.background('img/start.png', [0,0])
bird_image = pygame.image.load("img/bird.png")







# player vars
direction = ""
player_scale = 7 
player_image_width = 13 * player_scale
player_image_height = 27 * player_scale
location = [200, 200]
player_rect = pygame.Rect(location[0], location[1], player_image_width, player_image_height)
momentum = 0
left_right_speed = 10
player_frames = 3
player_sheet_image = pygame.image.load('img/player.png').convert_alpha()
zero_start = 0
right_end = 0 # 27 when done
left_end = 60 # second number 70
still_end = 30 # first numer 13 0 frames 
player_right_sheet = ss.SpriteSheet(player_sheet_image, 13, 25, player_scale, black, zero_start, right_end)
player_left_sheet = ss.SpriteSheet(player_sheet_image, 13, 60, player_scale, black, zero_start, left_end)
player_still_sheet = ss.SpriteSheet(player_sheet_image, 13, 25, player_scale, black, zero_start, still_end)
player_right_frames_list = []
player_left_frames_list = []
player_still_frames_list = []
player_frames = 3
player_frame_count = 0
for i in range(player_frames):
    frame_0 = player_right_sheet.get_image(i, 12, 56, player_scale, black, zero_start, right_end) # every player frame is 10 * 27
    player_right_frames_list.append(frame_0)

for i in range(player_frames):
    frame_0 = player_left_sheet.get_image(i, 12, 56, player_scale, black, zero_start, left_end) # every player frame is 10 * 27
    player_left_frames_list.append(frame_0)

for i in range(player_frames):
    frame_0 = player_still_sheet.get_image(i, 12, 56, player_scale, black, zero_start, still_end) # every player frame is 10 * 27
    player_still_frames_list.append(frame_0)

player_image = player_right_sheet
prev_frame_delay = 0
frame_delay = 3




# platform vars
prev_plat_time = 10
prev_time =  0
plat_list = []
plat_spacing = 11
plat_giggle_start = 5
plat_giggle_end = 10
rand_plat_time_start = 10
rand_plat_time_end = 20
plat_x_rand = 400
plat_y_rand = 800
plat_width  = 10 
plat_len = 200




# movemnt vars
moving_right = False
moving_left = False
jumping = False
jump_number = 0
can_jump = False







# number of platforms and first platform for start screen and toliet rect
count = 0
start_plat = platforms.platform("start", screen, 0, 960, screen_size[0]+ 10000, plat_width)
plat_list.append(start_plat)
toliet_rect = platforms.platform("toliet", screen, 1450, 680, 200, 100)
plat_list.append(toliet_rect)
# toliet = pygame.draw.rect(screen, [0,0,0], toliet_rect)





# loop and gameover state
loop = 1
gameover = False





# jumping vars
floatting = False
jump_height = 100
fall_speed = 15
jump_count = 10





# tank vars
tank_x = 1800
tank_y = 100
bullet_color = [255,0,0]
tank = tank.tank(screen, tank_image, bullet_image, tank_x, tank_y)
prev_bullet_time = 10
tank.init_bullet(bullet_color)
first = True
rand_bullet_time_start = 1
rand_bullet_time_end = 2
bullet_speed = 10
tank_move_speed = 10






# bird vars 
bird_list = []
prev_bird_time = 10
bird_move_speed = 20
bird_rand_location_start = 400
bird_rand_location_end = 800
bird_rand_start = 1 * fps
bird_rand_end = 5 * fps
new_bird = bird.bird(screen, bird_image, screen_size[0], random.randint(bird_rand_location_start,bird_rand_location_end))







# score vars
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 150)
score = -1
score_color = [255,255,0]
score_location = (600,0)







# insturction vars
pygame.font.init()
instruction_text = [ ["Move with arrow keys or 'W A S D'", 50, 150],
                    ["Jump with space bar. esc to quit", 50, 200],
                    ["That toilet is looking weird,", 50, 430], 
                    ["jump in and see what what happens", 50, 480]
                   ]
instruction_color = [122,92,1]
font_style = "tlwgtypewriter"
text_size = 70
time_delay = 0.0
prev_time_delay = 0





# init background music to loop forever
pygame.mixer.music.load("audio/backgroundmusic.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)




# intit sound stuff and play background music
intro = pygame.mixer.Sound("audio/intro.mp3")
poopy_water = pygame.mixer.Sound("audio/poopy_water.mp3")
check_out_the_pipes = pygame.mixer.Sound("audio/check_out_the_pipes.mp3")
jump = pygame.mixer.Sound("audio/jump.wav")
jump.set_volume(0.5)
pygame.mixer.Sound.play(intro)
rand_voice_line_start = 0
rand_voice_line_end = 700
voice_line_1 = 1




# movement for instruction screen
movement_control = movement.movement(screen, left_right_speed, location, 
                player_image_width, player_image_width, player_right_sheet, 
                player_left_sheet, player_still_sheet, start_background, 
                player_image, plat_list, player_rect, clock, fps, "img/start.png", player_image_height)





# start instance of moving controls
start_inst = instructions_screen.instruction_screen(screen, start_background, player_image, player_image_width, player_image_height, location, 
                 font_style, instruction_text, instruction_color, left_right_speed, clock, text_size, 
                 time_delay, player_right_sheet, player_left_sheet, player_still_sheet, movement_control, player_rect)


