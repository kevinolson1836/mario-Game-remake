import pygame
import random
import time
# bird class
class bird():
    # init bird 
    def __init__(self, screen, img, location_x, location_y):
        self.bird_location = [location_x, location_y]
        self.screen = screen
        self.bird_image = img
        self.screen_size = list(screen.get_size())
 
    #  move the bird
    def move(self, speed):
        self.bird_location = [self.bird_location[0]-speed, self.bird_location[1]]
        self.screen.blit(self.bird_image, self.bird_location)

    # draw the bird on screen
    def draw(self):
        # self.bird = pygame.draw.rect(self.screen, [0,0,0], pygame.Rect(self.bird_location[0]+7, self.bird_location[1]+7, 30, 30))
        self.screen.blit(self.bird_image, (self.bird_location[0], self.bird_location[1]))
    
    # return bird rect
    def get_bird_location(self):
        return(pygame.Rect(self.bird_location[0], self.bird_location[1], self.bird_image.get_width(), self.bird_image.get_height()))

    def print_debug(self):
        print("\tbird x location: " + str(self.bird_location[0]))
        print("\tbird y location: " + str(self.bird_location[1]))
        print()
    
    def random_timed_bird(self, start, end, frame_count, prev_time, fps):
         # randomly make new bird 
        if random.randint(start, end) < frame_count - prev_time: 
            prev_time = frame_count + fps
            new_bird = bird(self.screen, self.bird_image, self.screen_size[0], random.randint(start,end))
            new_bird.draw()
            return(new_bird)
        else:
            return(0)
