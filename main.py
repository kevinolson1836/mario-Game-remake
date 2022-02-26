import pygame
from pygame.locals import *
import random
import time


# background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# tank class
class tank():
    # init tank 
    def __init__(self, screen, location_x, location_y):
        self.tank_location = [location_x, location_y]
        self.tank_left = True
        self.screen = screen
 
    #  move the tank left to right
    def move(self, speed):
        if self.tank_left == True:
            self.tank_location[0] -= speed
            if self.tank_location[0] < 0:
                self.tank_left = False
        else:
            self.tank_location[0] += speed
            if self.tank_location[0] > 1900:
                self.tank_left = True
        screen.blit(tank_image, self.tank_location)

    #  init bullet
    def init_bullet(self, r, g, b):
        self.bullet_x = self.tank_location[0]
        self.bullet_y = self.tank_location[1]
        self.r = r
        self.g = g
        self.b = b 

    # draw the tank on screen
    def draw(self):
        self.shot = pygame.draw.rect(self.screen, [self.r,self.g,self.b], pygame.Rect(self.bullet_x, self.bullet_y+100, 50, 50))
        screen.blit(bullet_image, (self.bullet_x-15, self.bullet_y+60))


    # move bullet down
    def move_bullet(self, speed):
        self.bullet_y += speed
        self.draw()


    #  randomly move tank on screen, used on gameover
    def move_rand(self, speed):
        self.tank_location[0] = random.randint(0,speed)
        self.tank_location[1] = random.randint(0,speed)
        screen.blit(player_image, self.tank_location)
        self.draw()
        
    # return tank rect
    def rect(self):
        return (self.shot)

# class for platforms
class platform:
    #  draw platform
    def draw(self):
        self.rect = pygame.draw.rect(self.screen, [0,0,0], pygame.Rect(self.xpos, self.ypos, self.xwidth, self.ywidth))

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

    # plat x,y cords
    def get_pos(self):
        return(self.xpos, self.ypos)

    # print dbug info
    def print_debug(self):
        print("name: " + str(self.name))
        print("xpos: " + str(self.xpos))
        print("ypos: " + str(self.ypos))
        print("xwidth: " + str(self.xwidth))
        print("ywidth: " + str(self.ywidth))
        print()



# init pygame
pygame.init()
clock = pygame.time.Clock()
WINDOW_SIZE = (1400, 1000)
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = list(screen.get_size())

# load sprites
player_image = pygame.image.load("player.png")
bullet_image = pygame.image.load("fireball.png")
tank_image = pygame.image.load("tank.png")
BackGround = Background('sewer.png', [0,0])


# player vars
location = [200, 200]
player_rect = pygame.Rect(location[0], location[1], player_image.get_width(), player_image.get_height())
momentum = 0


# movemnt vars
moving_right = False
moving_left = False
jumping = False
jump_number = 0
can_jump = False

# platform vars
prev_plat_time = 0
prev_time =  time.time()
plat_list = []

# number of platforms and first platform
count = 0
start_plat = platform("start", screen, 0, 700, screen_size[0],10)
plat_list.append(start_plat)


# loop and gameover state
loop = 1
gameover = False

# init background music
pygame.mixer.music.load("mario.mp3")
pygame.mixer.music.play()

# jumping vars
floatting = False

# tank vars
tank = tank(screen, 1800,100)
prev_bullet_time = 0
tank.init_bullet(255,0,0)
first = True

# score vars
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 150)
score = 0


while loop:

    # game over code 
    if gameover == True:
        BackGround = Background('gameover.jpg', [random.randint(-1000,1000),random.randint(-1000,1000)])
        screen.blit(BackGround.image, BackGround.rect)
        tank.move_rand(1000)
        
        # random bullets falling
        if random.randint(1,1) < time.time() - prev_bullet_time: 
            prev_bullet_time = time.time()
            tank.init_bullet(random.randint(0,255),random.randint(0,255),random.randint(0,255))
       
        # move bullets    
        tank.move_bullet(10)

        # start game over music
        if first == True:
            pygame.mixer.music.load("gameover.mp3")
            pygame.mixer.music.play()
            first = False

        # score 
        screen.blit(textsurface,(600,0))


    else:
        # update the score
        textsurface = myfont.render("score:  " + str(score), False, (255, 100, 0))

        # draw background
        screen.blit(BackGround.image, BackGround.rect)
        
        # draw player and tank images 
        screen.blit(player_image, location)

        # score 
        screen.blit(textsurface,(600,0))

        # tank movement for bouncing
        tank.move(10)
        # tank.init_bullet()
        if random.randint(1,1) < time.time() - prev_bullet_time: 
            prev_bullet_time = time.time()
            tank.init_bullet(255,0,0)
            
            
        # for x in bullet_list:
        tank.move_bullet(20)
        if player_rect.colliderect(tank):
            gameover = True
            
        # 

        # every random 1-1 second  make new platform
        if random.randint(1,1) < time.time() - prev_plat_time: 
            prev_plat_time = time.time()
            count += 1
            plat = platform(count, screen, screen_size[0], random.randint(400,800), 200,10)
            plat.draw()
            plat_list.append(plat)
            
        # move all platforms with for loop
        for x in range(len(plat_list)):
            plat_list[x].move(random.randint(10,20))
            plat_list[x].draw()

        # check if the player collides with the platform 
        for x in range(len(plat_list)):
            if player_rect.colliderect(plat_list[x].rect):
                # update score 
                score += plat_list[x].score()
                # set player pos to top of platform
                if location[1] > plat_list[x].ypos - player_image.get_height():    
                    location[1] = plat_list[x].ypos - player_image.get_height() +11
                    floatting = True
                    momentum = 0
                else:
                    floaing = False
                can_jump = True
            else:
                if x == 0:
                    # if player bottom of screen end game
                    if player_rect.y > WINDOW_SIZE[1] + player_image.get_height() - 110:
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
            location[0] += 16

        # left movemnt 
        if moving_left == True:
            location[0] -= 16

        # jumping locgic
        if jumping == True:
            if jump_number < 0:
                jumping = False
                can_jump = False
            else: 
                can_jump = False
                jump_number -= 1
            if can_jump:
                jump_number = 10
            location[1] -= 100
            momentum = -15
            

    #  key management  
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                # quit game
                loop = 0
            if event.key == K_ESCAPE:
                # quit game
                loop = 0
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_SPACE:
                if can_jump:
                    can_jump = False
                    jumping = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_SPACE:
                jumping = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()