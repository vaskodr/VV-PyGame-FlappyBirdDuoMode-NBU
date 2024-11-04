import pygame
import random

class Pipe:
    def __init__(self, screen):
        self.pipe_surface = pygame.image.load('assets/pipe-green.png')
        self.pipe_surface = pygame.transform.scale(self.pipe_surface, (70, 250))
        self.pipe_list = []
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1400)
        self.pipe_height = [200, 225, 250, 275, 300, 325, 350, 360]
        self.screen = screen

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(midtop=(450, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(midbottom=(450, random_pipe_pos - 150))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5
        self.pipe_list = [pipe for pipe in self.pipe_list if pipe.right > -50]

    def draw_pipes(self):
        for pipe in self.pipe_list:
            if pipe.bottom >= 400:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)