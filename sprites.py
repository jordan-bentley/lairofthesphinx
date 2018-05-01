"""
Creates sprites for collision purposes
"""
import pygame

class Wall(pygame.sprite.Sprite):
    """
    Creates wall sprite with image parameter and coordinates
    """
    def __init__(self, image, coor):
        """
        :param image: image is png
        :param coor:  coordinates are tuple in form (x_coordinate, y_coordinate)
        """
        pygame.sprite.Sprite.__init__(self)     #Initializes sprite object using sprite library in Pygame
        self.image = image
        self.rect = self.image.get_rect()       #Gets rectangle sizes from image size
        self.rect.x = coor[0] + 64              #Sets x location
        self.rect.y = coor[1]                   #Sets y location
        self.rect.h = 64                        #Sets height
        self.rect.w = 64                        #Sets width

class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 377
        self.rect.y = 223
        self.rect.h = 30
        self.rect.w = 20

class Floor(pygame.sprite.Sprite):
    def __init__(self, image, coor):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coor[0] + 64
        self.rect.y = coor[1]

class Door(pygame.sprite.Sprite):
    def __init__(self, image, coor):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = coor[0] + 64
        self.rect.y = coor[1]
        self.rect.h = 64
        self.rect.w = 64