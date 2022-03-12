
import pygame
from pygame.locals import *
import random
import time
import sys
from  vars import *

# todo:
    # add some rats to go with the voice line
    # score board persistent over time. maybe use a database 
    # hit boxes seem to be a bit to big. idk if possible to get pixle perfect.helpful link: https://stackoverflow.com/questions/46862739/sprite-mask-collision-problems-in-pygame
    # make a real endding to the game, just a simple game over screen with leadorboards and retry / quit
    # add a real story line to game, some sort of toleit in a lab 
    # other 'games' in the game, like mini games for getting x amount of score
    # clean up code. a few unneeded vars, probably can change up some stuff to make it less lines
    # jump gravity seems to low or slow on main game loop, maybe its the game laggy for some reason, idk

# debug stuff
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        debug = True
        print("debug enabled")

# start screeen with instructions 
start_loop = 1
while start_loop:
    # return 1 when nothing. 0, momentum, move left, move right when in toleit hitbox
    if debug:
        start_loop = start_inst.move(debug=True)
    else:
        start_loop = start_inst.move()


# remove toleit rect from list
for x in range(len(plat_list)):
    if plat_list[x].get_name() == "toliet":
        plat_list.pop(x)

# number of platforms and first platform
count = 0
start_plat = platforms.platform("start", screen, 0, 700, screen_size[0], plat_width)
plat_list.append(start_plat)

# intro over, clean up intro bits
pygame.mixer.Sound.stop(intro)
pygame.mixer.Sound.play(poopy_water)

# move player to starting location
location = [200,200]

inst = movement_control.update_backround_img(background1, "img/sewer.png")
# main game loop
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
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # quit game
                if event.key == K_ESCAPE:
                    exit()

    else:
        # movement_control.move()
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
        if direction == "right":
            screen.blit(player_right_sheet.animate(player_frame_count), location)    
        elif direction == "left":
            screen.blit(player_left_sheet.animate(player_frame_count), location)     
        else:
            screen.blit(player_still_sheet.animate(1), location)    
        if debug:
            movement_control.move_updated_list(screen, plat_list, player_rect, location, background1, debug = True)
        else:
            movement_control.move_updated_list(screen, plat_list, player_rect, location, background1)
            
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
        if random.randint(rand_plat_time_start + int(fps), rand_plat_time_end + int(fps)) < frame_count - prev_plat_time: 
            prev_plat_time = frame_count + fps
            count += 1
            plat = platforms.platform(count, screen, screen_size[0], random.randint(plat_x_rand, plat_y_rand), plat_len, plat_width)
            plat.draw()
            plat_list.append(plat)
            
        # move all platforms with for loop
        for x in range(len(plat_list)):
            plat_list[x].move(random.randint(plat_giggle_start, plat_giggle_end))
            plat_list[x].draw()
            # print(plat_list)

    if debug == True:
        # print("player momentum: " + str(momentum))
        print("****************END OF DEBUG**********",end="\n\n\n\n\n")
        # move player to top left for debugging 
        location[0] = 1
        location[1] = 1
        player_rect.x = location[0]
        player_rect.y = location[1]
    
    pygame.display.update()
    clock.tick()
    frame_count += 1
    fps = clock.get_fps()
    # print(fps)

pygame.quit()