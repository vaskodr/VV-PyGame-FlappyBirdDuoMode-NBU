import pygame

class Floor:
    def __init__(self, screen):
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_surface = pygame.transform.scale(self.floor_surface, (400, 100))
        self.floor_x = 0
        self.screen = screen

    def draw(self):
        self.screen.blit(self.floor_surface, (self.floor_x, 400))
        self.screen.blit(self.floor_surface, (self.floor_x + 400, 400))