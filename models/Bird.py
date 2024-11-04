import pygame

class Bird:
    def __init__(self, screen, downflap_pic, midflap_pic, upflap_pic, x, y):
        self.bird_downflap = pygame.transform.scale(pygame.image.load(downflap_pic).convert_alpha(),
                                                    (35, 25))
        self.bird_midflap = pygame.transform.scale(pygame.image.load(midflap_pic).convert_alpha(),
                                                   (35, 25))
        self.bird_upflap = pygame.transform.scale(pygame.image.load(upflap_pic).convert_alpha(),
                                                  (35, 25))
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(x, y))
        self.bird_movement = 0
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)
        self.screen = screen

    def update_movement(self):
        self.bird_movement += 0.5
        rotated_bird = self.rotate_bird()
        self.bird_rect.centery += self.bird_movement
        self.screen.blit(rotated_bird, self.bird_rect)

    def rotate_bird(self):
        new_bird = pygame.transform.rotozoom(self.bird_surface, -self.bird_movement * 3, 1)
        return new_bird

    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
        return new_bird, new_bird_rect