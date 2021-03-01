'''
|----------------------------|--------------------------------------------------|
|Game Name:                  |The Hanoi Tower                                   |
|----------------------------|--------------------------------------------------|
|Implementation Platform:    |pygame                                            |
|----------------------------|--------------------------------------------------|
|Manual/Auto:                |Manual                                            |
|----------------------------|--------------------------------------------------|
|User Guide:                 |Press key "1","2","3" to move the discs           |
|                            |change "ORDER" to change the number of discs      |
|                            |change "INC" to change the speed that discs move  |
|----------------------------|--------------------------------------------------|
'''
import pygame as pg
import math

ORDER = 6 #number of discs/game order
INC = 100 #determines how fast the disc moves

DISC_COLOR = (33,159,213) #color of discs
DISC_THICK = 30 #thickness of discs
SIDE_COLOR = (16,63,145) #color of the silhouette of discs
DISC_MAX_LEN = 200 #max length of the discs
BG_COLOR = (1,22,39) #color of background
PIL_COLOR = (255,215,19) #color of pillars
LINE_COLOR = (133,230,149) #color of the ground line
Y_UP = 100 #height of the fly-position of the discs
INC = 5 #determines how fast the disc moves


class Disc(object):
    '''
    this class is for every disc
    '''

    window = None #window the discs are in
    font = None #text font that the discs adopt 

    def __init__(self,idx,window,h,w,x,y):
        '''
        @idx: the index of the disc,which indicates the size of it
        @window: window the discs are in
        @h: height of disc
        @w: width of disc
        @x: x coordinate of disc
        @y: y coordinate of disc
        '''
        self.idx = idx
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.new_x = self.x
        self.new_y = self.y
        self.__busy = False
        Disc.window = window
        Disc.font = pg.font.SysFont('Comic Sans MS',20)


    def ready(self,src_pil):
        '''
        this method grants a disc to be ready to move,and the disc will be lift up
        @src_pil: source pillar that the disc is originally on
        '''
        if self.__busy:
            print("warning:cannot lift object while a command is suspended")
            return False
        self.__busy = True
        self.new_y = Y_UP
        src_pil.eject()
        return True


    def move(self,dst_pil):
        '''
        this method grants a disc to move to another pillar
        @dst_pil: destination pillar that the disc move to
        '''
        if self.__busy:
            print("warning:cannot move object while a command is suspended")
            return False

        if self.idx > dst_pil.top_size:
            self.__busy = True
            self.new_x = dst_pil.x_pos - self.w/2
            self.new_y = dst_pil.y_top - DISC_THICK
            dst_pil.inject(self.idx)
            return True
        else:
            print("warning:action is against the game rule")
            return False


    def update(self):
        ''''
        this method updates the position and shape of the disc
        '''
        if self.x != self.new_x:
            if self.y != Y_UP:
                print("error occurs when moving")
            else:
                if self.x < self.new_x:
                    if self.new_x - self.x < INC:
                        self.x = self.new_x
                    else:
                        self.x += INC
                else:
                    if self.x - self.new_x < INC:
                        self.x = self.new_x
                    else:
                        self.x -= INC
        else:
            if self.y != self.new_y:
                if self.y < self.new_y:
                    if self.new_y - self.y < INC:
                        self.y = self.new_y
                    else:
                        self.y += INC
                else:
                    if self.y - self.new_y < INC:
                        self.y = self.new_y
                    else:
                        self.y -= INC
            else:
                self.__busy = False
        self.draw()


    def draw(self):
        '''
        this method draws a disc
        '''
        pg.draw.rect(Disc.window,DISC_COLOR,(self.x+15,self.y,self.w-30,self.h))
        pg.draw.ellipse(Disc.window,DISC_COLOR,(self.x,self.y,30,30))
        pg.draw.ellipse(Disc.window,DISC_COLOR,(self.x+self.w-30,self.y,30,30))
        pg.draw.arc(Disc.window,SIDE_COLOR,(self.x,self.y,30,30),math.pi/2,-math.pi/2,2)
        pg.draw.arc(Disc.window,SIDE_COLOR,(self.x+self.w-30,self.y,30,30),-math.pi/2,math.pi/2,2)
        pg.draw.line(Disc.window,SIDE_COLOR,
                        (self.x+15,self.y),(self.x+self.w-15,self.y),2)
        pg.draw.line(Disc.window,SIDE_COLOR,
                        (self.x+15,self.y+self.h),(self.x+self.w-15,self.y+self.h),2)
        
        text = Disc.font.render(str(self.idx+1), True, (255,255,255))
        Disc.window.blit(text,(self.x+self.w/2-7,self.y))



class Pillar(object):
    '''
    this class is for every pillar
    '''

    def __init__(self,idx,top_size,y_top,x_pos):
        '''
        @idx: the index of the pillar,0-left,1-middle,2-right
        @top_size: the size of the top disc on the pillar
        @y_top: the y coordinate of the top disc on the pillar
        @x_pos: the x coordinate of the pillar
        '''
        self.idx = idx
        self.top_size = top_size
        self.y_top = y_top
        self.x_pos = x_pos
        self.body = []
    
    def inject(self,idx):
        '''
        this method updates the pillar when a dsic lands on it
        @idx: the index(size) of the pillar that lands
        '''
        self.top_size = idx
        self.body.append(idx)
        self.y_top -= DISC_THICK
        

    def eject(self):
        '''
        this method updates the pillar when a disc leaves it
        '''
        self.body.pop()
        if len(self.body) == 0:
            self.top_size = -1
        else:
            self.top_size = self.body[-1]
        self.y_top += DISC_THICK


def game_init(order,window):
    '''
    this function initializes the game
    @order: the order of the game,also the number of discs
    @window: the window that the game plays in
    '''
    pg.font.init()
    disc = []
    pil = []
    indent = (200-45)//(order-1)
    for i in range(order):
        temp = Disc(i,window,DISC_THICK,DISC_MAX_LEN-i*indent,
                    200-(DISC_MAX_LEN-i*indent)/2,550-(i+1)*DISC_THICK)
        disc.append(temp)
        disc[i].draw()

    for i in range(3):
        temp = Pillar(i,-1,550,200*(i+1))
        pil.append(temp)

    for i in range(order):
        pil[0].body.append(i)
    pil[0].top_size = order-1
    pil[0].y_top -= order*DISC_THICK
    return disc,pil


def window_init():
    '''
    this function initializes the window and returns it
    '''
    pg.init()
    pg.display.set_caption('Hanoi Game')
    window = pg.display.set_mode((800,600))
    window.fill(BG_COLOR)
    pg.draw.rect(window,LINE_COLOR,(0,550,800,1))
    pg.draw.rect(window,PIL_COLOR,(200-5,200,10,350))
    pg.draw.rect(window,PIL_COLOR,(400-5,200,10,350))
    pg.draw.rect(window,PIL_COLOR,(600-5,200,10,350))
    pg.display.flip()
    return window


def draw_background(window):
    '''
    this function draws the background of the game
    @window: the window which the background is in
    '''
    window.fill(BG_COLOR)
    pg.draw.rect(window,LINE_COLOR,(0,550,800,1))
    pg.draw.rect(window,PIL_COLOR,(200-5,200,10,350))
    pg.draw.rect(window,PIL_COLOR,(400-5,200,10,350))
    pg.draw.rect(window,PIL_COLOR,(600-5,200,10,350))



if __name__ == "__main__":

    window = window_init()
    disc,pil = game_init(ORDER,window)
    pg.display.flip()
    sus_disc = None
    sus_flag = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            
            if event.type == pg.KEYDOWN:
                index = chr(event.key)

                if index != "1" and index != "2" and index != "3":
                    print("warning:invalid key action")
                else:
                    index = int(index)-1
                    if sus_flag:
                        if sus_disc.move(pil[index]):
                            sus_flag = False
                    else:
                        temp_pil = pil[index]
                        if len(temp_pil.body) == 0:
                            print("empty pillar")
                        else:
                            sus_disc = disc[temp_pil.top_size]
                            if disc[temp_pil.top_size].ready(temp_pil):
                                sus_flag = True


        draw_background(window)
        for i in range(ORDER):
            disc[i].update()
        pg.display.update()
