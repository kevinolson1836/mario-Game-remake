import pygame
import random

# tank class
class tank():
    # init tank 
    def __init__(self, screen, tank_img, bullet_image, location_x, location_y):
        self.tank_location = [location_x, location_y]
        self.tank_left = True
        self.screen = screen
        self.tank_img = tank_img
        self.bullet_image = bullet_image

    #  move the tank left to right
    def move(self, speed):
        if self.tank_left == True:
            self.tank_location[0] -= speed
            if self.tank_location[0] < 40:
                self.tank_left = False
        else:
            self.tank_location[0] += speed
            if self.tank_location[0] > 1900:
                self.tank_left = True
        self.screen.blit(self.tank_img, self.tank_location)

    #  init bullet
    def init_bullet(self, color):
        self.bullet_x = self.tank_location[0]
        self.bullet_y = self.tank_location[1]
        self.r = color[0]
        self.g = color[1]
        self.b = color[2]

    # draw the tank on screen
    def draw(self):
        # self.shot = pygame.draw.rect(self.screen, [self.r,self.g,self.b], pygame.Rect(self.bullet_x+20, self.bullet_y+80 , 20, 20))
        self.screen.blit(self.bullet_image, (self.bullet_x-15, self.bullet_y+60))

    def bullet_location(self):
        return(pygame.Rect(self.bullet_x, self.bullet_y, self.bullet_image.get_width(), self.bullet_image.get_height()))

    # move bullet down
    def move_bullet(self, speed):
        self.bullet_y += speed
        self.draw()

    #  randomly move tank on screen, used on gameover
    def move_rand(self, speed):
        self.tank_location[0] = random.randint(0,speed)
        self.tank_location[1] = random.randint(0,speed)
        self.screen.blit(self.tank_img, self.tank_location)
        self.draw()
        
    # return tank rect
    def rect(self):
        return (self.shot)

    def print_debug(self):
        print("\txpos: " + str(self.tank_location[0]))
        print("\typos: " + str(self.tank_location[1]))
        print("\txwidth: " + str(self.bullet_image.get_width()))
        print("\tywidth: " + str(self.bullet_image.get_height()))
        print("\tbullet x location: " + str(self.bullet_x))
        print("\tbullet y location: " + str(self.bullet_y))
        print()