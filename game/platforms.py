import pygame

# # class for platforms
class platform:
    #  draw platform
    def draw(self):
        self.rect = pygame.draw.rect(self.screen, [0,0,0], pygame.Rect(self.xpos, self.ypos-20, self.xwidth, self.ywidth))
        # pygame.display.update()

    # init platform vars
    def __init__(self, name, screen, xpos, ypos, xwidth, ywidth):
        self.name = name
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.xwidth = xwidth
        self.ywidth = ywidth
        self.add_score = True
        self.draw()

    #  score logic
    def score(self):
        if self.add_score == True:
            self.add_score = False
            return 1
        else:
            return 0

    # move platform
    def move(self, speed):
        self.xpos -= speed
        self.draw()
    
    # return platform rect
    def rect(self):
        return (self.rect)

    # platform name
    def print_name(self):
        print(self.name)

    # return name
    def get_name(self):
        return(self.name)
    
    # plat x,y cords
    def get_pos(self):
        return(self.xpos, self.ypos)

    # print dbug info
    def print_debug(self):
        print("\tname: " + str(self.name))
        print("\txpos: " + str(self.xpos))
        print("\typos: " + str(self.ypos))
        print("\txwidth: " + str(self.xwidth))
        print("\tywidth: " + str(self.ywidth))
        print()