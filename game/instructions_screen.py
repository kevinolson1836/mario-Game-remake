from matplotlib import scale
import pygame
from pygame.locals import *
import math
import background
import platforms
import time
import movement

# class to make the instuction screen
class instruction_screen:
    def __init__(self, screen, background_image, player_image, player_image_width, player_image_height,
                location, font, insturctions, instruction_color, left_right_speed, clock, text_size,
                time_delay, player_right_sheet, player_left_sheet, player_still_sheet, movement_driver, player_rect):
        self.screen = screen                        # main screen
        self.background_image = background_image    # background image
        self.background_rect = background.background("img/start.png", [0,0]) # background rect
        self.player_image = player_image            # player image
        self.insturctions = insturctions            # should be a list. [instruction text, x_cord, y_cord]
        self.font = font                            # font style
        self.instruction_color = instruction_color  # color of text
        self.location = location
        self.player_rect = player_rect
        self.plat_list = [] 
        self.start_plat = platforms.platform("start", self.screen, 0, 800, 2000, 50)
        self.plat_list.append(self.start_plat)
        self.toliet_rect = platforms.platform("toliet", self.screen, 1450, 680, 200, 100)    #pygame.Rect(1450, 680, 200, 100)
        self.plat_list.append(self.toliet_rect)
        # self.plat_list.append(self.toliet_rect)
        self.left_right_speed = left_right_speed
        self.momentum = 0
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.jump_number = 0
        self.can_jump = True
        self.clock = clock
        self.text_size = text_size
        self.prev_time_delay = 0
        self.time_delay = time_delay
        self.player_frame_count = 0
        self.player_max_frame_count = 3
        self.player_image_width = player_image_width
        self.player_image_height = player_image_height
        self.frame_delay = 3
        self.frame_count = 0
        self.prev_time = 0
        self.player_right_sheet = player_right_sheet
        self.player_left_sheet = player_left_sheet
        self.player_still_sheet = player_still_sheet
        self.direction = ""

        self.movement_control = movement_driver

    def render_text(self):
        # make the text gitter
        if self.text_size > 70:
            self.text_size = 68
        pyfont = pygame.font.SysFont(self.font, math.floor(self.text_size), bold=True)
        if self.time_delay < time.time() - self.prev_time_delay:
            self.text_size += 0.1
            self.prev_time_delay = time.time()
        
        # blit screen with instrctuinos 
        for line in self.insturctions:
            location = [line[1], line[2]] 
            surface = pyfont.render(line[0], False, self.instruction_color)
            self.screen.blit(surface, location)


    def move(self, debug=False):
        if debug:
            self.movement_control_return = self.movement_control.move(debug=True)
        else:
            self.movement_control_return = self.movement_control.move()
        self.render_text()
        pygame.display.update()
        return(self.movement_control_return)