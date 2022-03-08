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

# todo:
    # some sort of config file
    # add a proper debugger??? 
    # score board persistent over time. maybe use a database 
    # hit boxes seem to be a bit to big. idk if possible to get pixle perfect.helpful link: https://stackoverflow.com/questions/46862739/sprite-mask-collision-problems-in-pygame
    # make a real endding to the game, just a simple game over screen with leadorboards and retry / quit
    # fix the bug with first time jummping a double jump, fix not allowing a doubble jump when walking off platform
    # add a real story line to game, some sort of toleit in a lab 
    # other 'games' in the game, like mini games for getting x amount of score
    # clean up code. a few unneeded vars, probably can change up some stuff to make it less lines
    # make more than one file to spilt up code for better orginazation. worked on a bit but still needs more

# debug stuff
debug = False
waiting = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        debug = True
        print("debug enabled")

# init pygame
pygame.init()
clock = pygame.time.Clock()
WINDOW_SIZE = (1400, 1000)
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = list(screen.get_size())
frame_count = 0
fps = 30
start_loop = True

# load sprites
player_image = pygame.image.load("img/player.png")
bullet_image = pygame.image.load("img/bullet.png")
tank_image = pygame.image.load("img/tank.png")
background1 = background.background('img/sewer.png', [0,0])
start_background = background.background('img/start.png', [0,0])
bird_image = pygame.image.load("img/bird.png")

# player vars
location = [200, 200]
player_rect = pygame.Rect(location[0], location[1], player_image.get_width(), player_image.get_height())
momentum = 0
left_right_speed = 16
player_hieght = 110

# movemnt vars
moving_right = False
moving_left = False
jumping = False
jump_number = 0
can_jump = False

# platform vars
prev_plat_time = 10
prev_time =  0
plat_list = []
plat_spacing = 11
plat_giggle_start = 10
plat_giggle_end = 20
rand_plat_time_start = (1)
rand_plat_time_end = (1)
plat_x_rand = 400
plat_y_rand = 800
plat_width  = 10 
plat_len = 200

# number of platforms and first platform for start screen and toliet rect
count = 0
start_plat = platforms.platform("start", screen, 0, 950, screen_size[0], plat_width)
plat_list.append(start_plat)
toliet_rect = pygame.Rect(1450, 680, 200, 100)
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
bird_move_speed = 50
bird_rand_location_start = 400
bird_rand_location_end = 800
bird_rand_start = 1 * fps
bird_rand_end = 5 * fps
new_bird = bird.bird(screen, bird_image, screen_size[0], random.randint(bird_rand_location_start,bird_rand_location_end))

# score vars
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 150)
score = -2
score_color = [255,255,0]
score_location = (600,0)

# insturction vars
pygame.font.init()
# instruction_text =  "Welcome to (game name)"
instruction_text2 = "Move with arrow keys or 'W A S D'"
instruction_text3 = "Jump with space bar"
instruction_text4 = "That toilet is looking weird,"
instruction_text5 = "jump in and see what what happens"
instruction_color = [122,92,1]
instruction_location =  (50,50)
instruction_location2 = (50,170)
instruction_location3 = (50,310)
instruction_location4 = (50,460)
instruction_location5 = (50,600)
text_size = 70
time_delay = 0.02
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



# start first screen loop
while start_loop:
    # blit background and player
    screen.blit(start_background.image, background1.rect)
    screen.blit(player_image, location)

    # insturctions. could use some clean up
    if text_size > 70:
        text_size = 68
    insturction_font = pygame.font.SysFont('tlwgtypewriter', math.floor(text_size), bold=True)
    if time_delay < time.time() - prev_time_delay:
        text_size += 0.2
        prev_time_delay = time.time()
    instruction_surface2 = insturction_font.render(instruction_text2, False, instruction_color)
    instruction_surface3 = insturction_font.render(instruction_text3, False, instruction_color)
    instruction_surface4 = insturction_font.render(instruction_text4, False, instruction_color)
    instruction_surface5 = insturction_font.render(instruction_text5, False, instruction_color)
    screen.blit(instruction_surface2, instruction_location2)
    screen.blit(instruction_surface3, instruction_location3)
    screen.blit(instruction_surface4, instruction_location4)
    screen.blit(instruction_surface5, instruction_location5)

    # update player location on screen   
    player_rect.x = location[0]
    player_rect.y = location[1]

    for x in range(len(plat_list)):
        if player_rect.colliderect(plat_list[x].rect):
            # update score 
            score += plat_list[x].score()
            # set player pos to top of platform
            if location[1] > plat_list[x].ypos - player_image.get_height():    
                location[1] = plat_list[x].ypos - player_image.get_height() + plat_spacing 
                floatting = True
                momentum = 0
            else:
                floaing = False
            can_jump = True
        else:
            if x == 0:
                # if player bottom of screen end game
                if player_rect.y > WINDOW_SIZE[1] + player_image.get_height() - player_hieght:
                    gameover = True
                # else make player fall
                else:
                    momentum += 1     
    location[1] += momentum

    if player_rect.colliderect(toliet_rect):
        start_loop = False
        location = [200, 200]

    if moving_right == True:
        location[0] += left_right_speed

        # left movemnt 
    if moving_left == True:
        location[0] -= left_right_speed

    # jumping locgic
    if jumping == True:
        if jump_number < 0:
            jumping = False
            can_jump = False
        else: 
            can_jump = False
            jump_number -= 1
        if can_jump:
            jump_number = jump_count
        location[1] -= jump_height
        momentum = -fall_speed
        
#  key management  
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # quit game
            if event.key == K_ESCAPE:
                exit()
            # move right
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
            # move left
            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
            # jump
            if event.key == K_SPACE:
                if can_jump:
                    can_jump = False
                    jumping = True           

        # keys stopped being pressed
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_SPACE:
                jumping = False

    # update screen
    pygame.display.update()
    clock.tick()

# number of platforms and first platform
count = 0
start_plat = platforms.platform("start", screen, 0, 700, screen_size[0], plat_width)
plat_list.append(start_plat)

# intro over, clean up intro bits
# kill starting plat
# move player to starting location
pygame.mixer.Sound.stop(intro)
pygame.mixer.Sound.play(poopy_water)

while loop:
    # game over code 
    if gameover == True:
        background1 = background.background('img/gameover.jpg', [random.randint(-1000,1000),random.randint(-1000,1000)])
        screen.blit(background1.image, background1.rect)
        tank.move_rand(1000)
        
        # random bullets falling
        if rand_bullet_time_start < frame_count - prev_bullet_time: 
            prev_bullet_time = frame_count
            bullet_color[0] = random.randint(0,255)
            bullet_color[1] = random.randint(0,255)
            bullet_color[2] = random.randint(0,255)
            tank.init_bullet(bullet_color)
       
        # move bullets    
        tank.move_bullet(bullet_speed)

        # start game over music
        if first == True:
            pygame.mixer.music.load("audio/gameover.mp3")
            pygame.mixer.music.play()
            first = False

        # score 
        screen.blit(score_surface,score_location)

    else:
        # print debug info
        if debug == True:
            # move player to top left for debugging
            location[0] = 1
            location[1] = 1
            player_rect.x = location[0]
            player_rect.y = location[1]
            print("****************START OF DEBUG**********")
            print("current FPS: ", end='')
            print(clock.get_fps())
            print("current frame: ", end='')
            print(frame_count)

        # random chance to play a voice line
        if random.randint(rand_voice_line_start,rand_voice_line_end) == voice_line_1:
            pygame.mixer.Sound.play(check_out_the_pipes)
            rand_voice_line_end += rand_voice_line_end

        # update the score
        score_surface = myfont.render("score:  " + str(score), False, score_color)

        # draw background
        screen.blit(background1.image, background1.rect)
        
        # draw player and tank images 
        screen.blit(player_image, location)

        # score 
        screen.blit(score_surface,(score_location))

        # tank movement for bouncing
        tank.move(tank_move_speed)

        # tank.init_bullet()
        if random.randint(rand_bullet_time_start, rand_bullet_time_end) < frame_count - prev_bullet_time:
            if fps != 0: 
                prev_bullet_time = frame_count + (fps * 2)
                tank.init_bullet(bullet_color)

        # end game if collided with bulet from tank
        tank.move_bullet(20)
        if player_rect.colliderect(tank.bullet_location()):
            if debug == True:
                    print(f"player collieded with BULLET:")
                    tank.print_debug()
                    print("player location: " + str(location))
            gameover = True

        # randomly make new bird 
        xbird = new_bird.random_timed_bird(bird_rand_location_start, bird_rand_location_end, frame_count, prev_bird_time, fps)
        if xbird != 0:
            prev_bird_time = frame_count + fps
            bird_list.append(xbird)

        # draw and move all birds
        for x in bird_list:
            x.move(bird_move_speed)
            x.draw()
            # gameover if collieded with bird
            if player_rect.colliderect(x.get_bird_location()):
                if debug == True:
                    print(f"player collieded with BIRD:")
                    x.print_debug()
                    print("player location: " + str(location))
                gameover = True


        # every random_plat_time  make new platform
        if random.randint(rand_plat_time_start, rand_plat_time_end) < frame_count - prev_plat_time: 
            prev_plat_time = frame_count + fps
            count += 1
            plat = platforms.platform(count, screen, screen_size[0], random.randint(plat_x_rand, plat_y_rand), plat_len, plat_width)
            plat.draw()
            plat_list.append(plat)
            
        # move all platforms with for loop
        for x in range(len(plat_list)):
            plat_list[x].move(random.randint(plat_giggle_start, plat_giggle_end))
            plat_list[x].draw()

        # check if the player collides with the platform 
        for x in range(len(plat_list)):
            if player_rect.colliderect(plat_list[x].rect):
                if debug == True:
                    print(f"player collieded with PLATFORM:")
                    plat_list[x].print_debug()
                    print("player location: " + str(location))
                # update score 
                score += plat_list[x].score()
                # set player pos to top of platform
                if location[1] > plat_list[x].ypos - player_image.get_height():    
                    location[1] = plat_list[x].ypos - player_image.get_height() + plat_spacing
                    floatting = True
                    momentum = 0
                else:
                    floaing = False
                can_jump = True
            else:
                if x == 0:
                    # if player bottom of screen end game
                    if player_rect.y > WINDOW_SIZE[1] + player_image.get_height() - player_hieght:
                        gameover = True
                    # else make player fall
                    else:
                        momentum += 1     
        location[1] += momentum

        # update player location on screen   
        player_rect.x = location[0]
        player_rect.y = location[1]
        
        # if off screen left end game
        if player_rect.x == 0:
            gameover = True
        # if xpos all the way to the right exit game
        if player_rect.x == screen_size[0]:
            gameover = True
        # right movement
        if moving_right == True:
            location[0] += left_right_speed

        # left movemnt 
        if moving_left == True:
            location[0] -= left_right_speed

        # jumping locgic
        if jumping == True:
            if jump_number < 0:
                pygame.mixer.Sound.play(jump)
                jumping = False
                can_jump = False
            else: 
                can_jump = False
                jump_number -= 1
            if can_jump:
                jump_number = jump_count
            location[1] -= jump_height
            momentum = -fall_speed
            
    #  key management  
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # quit game
            if event.key == K_ESCAPE:
                loop = 0
                if debug == True:
                    print("user quit game")
            # move right
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = True
            # move left
            if event.key == K_LEFT or event.key == K_a:
                moving_left = True
            # jump
            if event.key == K_SPACE:
                if can_jump:
                    can_jump = False
                    jumping = True           

        # keys stopped being pressed
        if event.type == KEYUP:
            if event.key == K_RIGHT or event.key == K_d:
                moving_right = False
            if event.key == K_LEFT or event.key == K_a:
                moving_left = False
            if event.key == K_SPACE:
                 jumping = False
    if debug == True:
        print("player momentum: " + str(momentum))
        print("****************END OF DEBUG**********",end="\n\n\n\n\n")
        # move player to top left for debugging 
        location[0] = 1
        location[1] = 1
        player_rect.x = location[0]
        player_rect.y = location[1]
            
    # update screen, advance clock, add frame to total count, update fps
    pygame.display.update()
    clock.tick()
    frame_count += 1
    fps = clock.get_fps()

# quit pygame
pygame.quit()