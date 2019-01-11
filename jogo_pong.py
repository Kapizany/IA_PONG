from pygame.locals import *
from itertools import cycle
import random
import sys
from numpy import math
from random import randint
import pygame
import time

sleep = [500] 

class Ball:
    x = 0
    y = 0
    step = 44
    
    def updateSleep(self):
        sleep[0] = sleep[0] + 20

    def __init__(self,x):
        self.x = x * self.step
        self.y = 0
 
    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 

    def createBall(self,x):
        self.x = x*self.step
        self.y = 0

    def update(self):
        self.y = self.y + 0.7*self.step


class Life:
    x = 0
    y = 0
    number = 0
    def __init__(self,number):
        self.number = number

    def draw(self, surface, image):
        for i in range(self.number):
            surface.blit(image,(self.x, self.y + i*25)) 

    def updateLife(self):
        self.number -= 1

    


class Player:
    step = 44
    x = 11*step
    y = 12
    direction = 0
    length = 3
 
    updateCountMax = 2
    updateCount = 0
 
    def __init__(self, length):
       self.length = length
    
 
    def update(self):
 
        # update position of board
        if self.direction == 0:
            self.x = self.x
        if self.direction == 1:
            self.x = self.x + self.step
        if self.direction == -1:
            self.x = self.x - self.step
 
 
 
    def moveRight(self):
        self.direction = 1
 
    def moveLeft(self):
        self.direction = -1
 
    def noMove(self):
        self.direction = 0
 
    def draw(self, surface, image):
        surface.blit(image,(self.x,self.y*self.step))
        for i in range(1,int(math.ceil(self.length /2))):
            surface.blit(image,(self.x + 1.5*i*self.step,self.y*self.step))
            surface.blit(image,(self.x - 1.5*i*self.step,self.y*self.step))


class Game:
    def wallCollision(self, y_ball, windowHeight):
        if y_ball >= windowHeight:
            print("Se Fudeu!")
            return True
        return False

    def caughtBall(self,x_player,y_player, x_ball, y_ball,playerWidth,playerHeight,ballWidth,ballHeight):
        if ((x_ball- ballWidth/2 < x_player + playerWidth/2 ) and (x_ball + ballWidth/2 > x_player - playerWidth/2)):
            if (y_ball + ballHeight/2 > y_player - playerHeight*0.4) and (y_ball - ballHeight/2 < y_player + playerHeight/2):
                return True
        return False

class App:
 
    windowWidth = 960
    windowHeight = 600
    ballWidth = 52
    ballHeight = 49
    playerWidth = 66*3
    playerHeight = 30
    lifeWidth = 20
    lifeHeight = 20
    player_length = 3
    player = 0
    ball = 0

 
    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._ball_surf = None
        self._life_surf = None
        self.game = Game()
        self.player = Player(self.player_length) 
        self.ball = Ball(randint(3,14))
        self.life = Life(3)
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
 
        pygame.display.set_caption('IA PONG')
        self._running = True
        self._image_surf = pygame.transform.scale(pygame.image.load("sipahi.jpg").convert(), (int(self.playerWidth/3),self.playerHeight))
        self._ball_surf = pygame.image.load("lua.png").convert()
        self._life_surf = pygame.transform.scale(self._ball_surf, (self.lifeWidth,self.lifeHeight))
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
 
    def on_loop(self):
        self.player.update()
        self.ball.update()
 
        # does player catch the ball?
        if self.game.caughtBall(self.player.x,self.player.y*self.ball.step,self.ball.x, self.ball.y,self.playerWidth,self.playerHeight,self.ballWidth,self.ballHeight):
            self.ball.updateSleep()
            self.ball.x = randint(3,15) * self.ball.step
            self.ball.y = 0
                
 
 
        # does ball collide with wall?
        if self.game.wallCollision(self.ball.y, self.windowHeight):
            print("You lose! Collision: ")
            print("x[0] (" + str(self.ball.x) + "," + str(self.ball.y) + ")")
            if self.life.number == 0:
                self._running = False
            else:
                self.life.updateLife()
            self.ball.createBall(randint(3,15))
            #print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
            #exit(0)
 
        pass
 
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.ball.draw(self._display_surf, self._ball_surf)
        self.life.draw(self._display_surf, self._life_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed() 
 
            if (keys[K_RIGHT]):
                self.player.moveRight()
 
            elif (keys[K_LEFT]):
                self.player.moveLeft()

            else:
                self.player.noMove()

            if (keys[K_ESCAPE]):
                self._running = False
 
            self.on_loop()
            self.on_render()
 
            time.sleep (50 /sleep[0])
        self.on_cleanup()
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()