import pygame
from pygame.locals import *
import random
pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

ground_scroll = 0
scroll_speed = 4
flying = False
gameOver= False
pipe_gap=125
last__pipe= pygame.time.get_ticks()-1500
player_score=0
pass_pipe=False
font=pygame.font.SysFont('Bauhaus 93',60)
white=(255,255,255)



bg= pygame.image.load('img/bg.png')
gr= pygame.image.load('img/gd.png')
btn_img=pygame.image.load("img/restart.png")

def draw_text(text,font,color,x,y):
    img=font.render(text,True,color)
    screen.blit(img,(x,y))


def reset():
    pipe_group.empty()
    flappy.rect.x=100
    flappy.rect.y=int(SCREEN_HEIGHT / 2)
    player_score=0
    return player_score



#Bird Class
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1 , 4):
            img= pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
    
    def update(self):
        if flying == True:
            self.vel += 0.9
            if self.vel > 8:
                self.vel=8
            if self.rect.bottom < 504:
                self.rect.y += int(self.vel)

        if gameOver == False:
            if pygame.mouse.get_pressed()[0]==1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked = False

            self.counter += 1 
            flap_coolDown = 5
            
            if self.counter >= flap_coolDown:
                self.counter=0
                self.index +=1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90) 
    
#Pipe Class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1: #top pipe
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft =[x, y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft =[x, y +int(pipe_gap/2)]
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill

#Restart class
class Button():
    
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.topleft = (x,y)
    def draw(self):
        restart=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1:
                restart=True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return restart


bird_group = pygame.sprite.Group()
pipe_group= pygame.sprite.Group()

flappy = Bird(100 , int(SCREEN_HEIGHT / 2))

bird_group.add(flappy)

button=Button(int(SCREEN_WIDTH/2)-70,int(SCREEN_HEIGHT/2),btn_img)

run = True
while run:

    clock.tick(60)
    
    screen.blit(bg , (0,0))

    
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    
    screen.blit(gr , (ground_scroll,504))

    #Score
    if len(pipe_group) >0:
        if bird_group.sprites()[0].rect.left >  pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right <  pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe=True
        if pass_pipe==True:
            if bird_group.sprites()[0].rect.left >  pipe_group.sprites()[0].rect.right:
                player_score+=1
                pass_pipe=False

    draw_text(str(player_score),font,white,int(SCREEN_WIDTH/2),20)


    #Look for collision
    if pygame.sprite.groupcollide(bird_group,pipe_group,False,False) or flappy.rect.top <0:
        gameOver=True

    if flappy.rect.bottom >= 504:
        gameOver = True
        flying=False


    if gameOver==False and flying:
        time_rnow=pygame.time.get_ticks()
        if time_rnow - last__pipe > 1500:
            pipe_height= random.randint(-100, 100)
            btm_pipe= Pipe(SCREEN_WIDTH , 250 + pipe_height , -1)
            top_pipe=  Pipe(SCREEN_WIDTH , 250 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last__pipe=time_rnow


        ground_scroll -= scroll_speed

        if abs(ground_scroll) > 615 : 
            ground_scroll=0
        pipe_group.update()

    #Restarting the game
    if gameOver==True:
       if button.draw():
           gameOver=False
           player_score=reset()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type== pygame.MOUSEBUTTONDOWN and flying == False and gameOver == False:
            flying = True

    pygame.display.update()
pygame.quit()