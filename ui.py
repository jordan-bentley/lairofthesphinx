import pygame, sys, glob
from pygame import *

h=400           #screen height
w=800           #screen width
pygame.font.init()  #creates font object for displaying text

screen = pygame.display.set_mode((w,h))     #creates screen object
scale = 64                                  #sets size for sprites
font = pygame.font.SysFont('Comic Sans MS', 14) #sets one font size
announce_font = pygame.font.SysFont('Comic Sans MS', 40)    #sets announcement font size

class UI():
    """
    Handling for the User Interface
    """
    def __init__(self):
        """
        initializes class variables
        """
        self.state = 0                                            #state 0 is alive, state 1 is dead
        self.alph = 0                                             #brightness of ui
        self.arrow_img = pygame.image.load("arrows.png")          #should load in image of arrow keys
        self.match = pygame.image.load("match.png")               #loads image of a match
        self.treas = pygame.image.load("treasure_ui.png")
        self.health_indicator = font.render('Health', False, (255,255,255)) #creates health bar text
        self.death_indicator = announce_font.render('You have died..', True, (0,0,0))   #creates death announcements
        self.try_again = announce_font.render('Would you like to try again? Y/N', True, (0,0,0))
        self.treasure_get = announce_font.render('You found a treasure!', True, (255, 255, 255))    #Treasure announcement
        #self.toggle_indicator = font.render('')
        self.toggle = False                                       #Toggle UI on or off


    def update_match(self, match_num):
        """
        :param match_num: Current matches in the player class. INT
        :return: Blits current match number on the screen in the top left side
        """
        x = 10
        y = 10
        for match in range(match_num):
            screen.blit(self.match, (x, y))
            x += 10

    def update_treasure(self, treas_num):
        x = -20
        y = 20
        for treasure in range(treas_num):
            screen.blit(self.treas, (x,y))
            x += 20

    def update_health(self, color, x, y, value, maxvalue):
        """
        :param color: Color of health bar
        :param x:   X coordinate of health bar
        :param y:   Y coordinate of health bar
        :param value: Current health
        :param maxvalue: Maximimum Health
        :return:    Blits current health bar to screen
        """
        xx = 0
        if value < 25:
            color = (153,0,0)
        curr_hp = int(max(min(value / float(maxvalue) * 100, 100), 0))
        pygame.draw.rect(screen, color, (x, y, curr_hp, 24), 0)
        pygame.draw.rect(screen, (255,255,255),(x,y, 100, 24), 1)
        screen.blit(self.health_indicator, ((x+28),(y+1)))
        xx += value / 100

    def arrows(self):
        """
        Method does not currently work.
        Designed to be controls shown on screen
        :return: Nothing
        """
        screen.blit(self.arrow_img, ((w-100),(h-100)))

    def tres_count(self, treas_num):
        self.survive_indicator = announce_font.render('You survived with ' + str(treas_num) + " treasures!", True, (0, 0, 0))


