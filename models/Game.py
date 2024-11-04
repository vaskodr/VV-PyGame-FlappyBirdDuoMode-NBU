import sys
import pygame
from models.Floor import Floor
from models.Bird import Bird
from models.Pipe import Pipe
from models.Score import Score


class Game:
    def __init__(self):
        self.winner = None
        pygame.init()
        pygame.display.set_caption("Flappy Bird with Modes")
        self.screen = pygame.display.set_mode((400, 500))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('Righteous-Regular.ttf', 20)

        self.gravity = 0.5
        self.game_active = True

        self.bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.bg_surface = pygame.transform.scale(self.bg_surface, (400, 500))

        self.floor = Floor(self.screen)
        self.pipe = Pipe(self.screen)
        self.bird1 = Bird(self.screen, 'assets/bluebird-downflap.png', 'assets/bluebird-midflap.png',
                          'assets/bluebird-upflap.png', 100, 200)
        self.bird2 = Bird(self.screen, 'assets/redbird-downflap.png', 'assets/redbird-midflap.png',
                          'assets/redbird-upflap.png', 150, 200)
        self.score = Score(self.screen, self.game_font)

    def check_collision(self, bird):
        for pipe in self.pipe.pipe_list:
            if bird.bird_rect.colliderect(pipe):
                pygame.mixer.Sound('audio/hit.wav').play()
                self.score.can_score = True
                return False

        if bird.bird_rect.top <= -100 or bird.bird_rect.bottom >= 400:
            self.score.can_score = True
            return False

        return True

    def main_menu(self):
        running = True
        while running:
            self.screen.blit(self.bg_surface, (0, 0))
            logo = pygame.image.load("assets/logo.png").convert_alpha()
            logo = pygame.transform.scale(logo, (280, 80))
            self.screen.blit(logo, (65, 80))
            self.floor.draw()
            # Display menu options
            menu_font = pygame.font.Font('Righteous-Regular.ttf', 30)
            single_mode_text = menu_font.render("1) SINGLE MODE (PRESS S)", True, (255, 255, 255))
            duo_mode_text = menu_font.render("2) DUO MODE (PRESS D)", True, (255, 255, 255))
            exit_text = menu_font.render("3) EXIT (PRESS EXIT)", True, (255, 255, 255))

            self.screen.blit(single_mode_text, (20, 200))
            self.screen.blit(duo_mode_text, (20, 250))
            self.screen.blit(exit_text, (45, 430))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.resetGame('Single')
                        self.run_single_mode()
                    elif event.key == pygame.K_d:
                        self.resetGame('Double')
                        self.run_duo_mode()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.clock.tick(30)

    def resetGame(self, mode):
        self.game_active = True
        self.pipe.pipe_list.clear()
        if mode == 'Single':
            self.bird1.bird_rect.center = (100, 250)
            self.bird1.bird_movement = 0
            self.score.score = 0
        elif mode == 'Double':
            self.bird1.bird_rect.center = (100, 200)
            self.bird1.bird_movement = 0
            self.bird2.bird_rect.center = (150, 200)
            self.bird2.bird_movement = 0

    def run_single_mode(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_active:
                        self.bird1.bird_movement = 0
                        self.bird1.bird_movement -= 10
                        pygame.mixer.Sound('audio/wing.wav').play()

                if not self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.resetGame('Single')
                        if event.key == pygame.K_m:
                            self.main_menu()
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                if event.type == self.pipe.SPAWNPIPE:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

                if event.type == self.bird1.BIRDFLAP:
                    if self.bird1.bird_index < 2:
                        self.bird1.bird_index += 1
                    else:
                        self.bird1.bird_index = 0

                    self.bird1.bird_surface, self.bird1.bird_rect = self.bird1.bird_animation()

                if event.type == self.score.SCOREEVENT:
                    self.score.score_sound_countdown -= 1
                    if self.score.score_sound_countdown <= 0:
                        self.score.score_sound_countdown = 100

            self.screen.blit(self.bg_surface, (0, 0))

            if self.game_active:
                self.bird1.update_movement()
                self.game_active = self.check_collision(self.bird1)
                self.pipe.move_pipes()
                self.pipe.draw_pipes()
                self.floor.floor_x -= 3
                self.floor.draw()
                if self.floor.floor_x <= -400:
                    self.floor.floor_x = 0
                self.score.pipe_score_check(self.pipe.pipe_list, pygame.mixer.Sound('audio/point.wav'))
                self.score.score_display('main_game', 'Single')
            else:
                self.floor.draw()
                self.menu_game_over()
                self.score.update_score()
                self.score.score_display('game_over', 'Single')

            pygame.display.update()
            self.clock.tick(45)

    def run_duo_mode(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            self.bird1.bird_movement = 0
                            self.bird1.bird_movement -= 10
                            pygame.mixer.Sound('audio/wing.wav').play()
                        if event.key == pygame.K_UP:
                            self.bird2.bird_movement = 0
                            self.bird2.bird_movement -= 10
                            pygame.mixer.Sound('audio/wing.wav').play()
                if not self.game_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.resetGame('Double')
                        if event.key == pygame.K_m:
                            self.main_menu()
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()

                if event.type == self.bird1.BIRDFLAP:
                    self.bird1.update_movement()

                if event.type == self.bird2.BIRDFLAP:
                    self.bird2.update_movement()

                if event.type == self.pipe.SPAWNPIPE:
                    self.pipe.pipe_list.extend(self.pipe.create_pipe())

            self.screen.blit(self.bg_surface, (0, 0))

            if self.game_active:
                self.bird1.update_movement()
                self.bird2.update_movement()
                if not self.check_collision(self.bird1):
                    self.game_active = False
                    self.winner = "Red bird"
                if not self.check_collision(self.bird2):
                    self.game_active = False
                    self.winner = "Blue bird"
                self.pipe.move_pipes()
                self.pipe.draw_pipes()
                self.floor.floor_x -= 3
                self.floor.draw()

                if self.floor.floor_x <= -400:
                    self.floor.floor_x = 0

            else:
                self.floor.draw()
                self.menu_game_over()
                self.score.score_display('game_over', 'Double', self.winner)

            pygame.display.update()
            self.clock.tick(60)

    def menu_game_over(self):
        game_over_menu_font = pygame.font.Font('Righteous-Regular.ttf', 40)
        reset = game_over_menu_font.render("Press R) - Reset ", True, (255, 255, 255))
        menu = game_over_menu_font.render("Press M) - Menu ", True, (255, 255, 255))
        exit_game = game_over_menu_font.render("Press ESC) - EXIT", True, (255, 255, 255))
        reset_rect = reset.get_rect(center=(200, 140))
        menu_rect = menu.get_rect(center=(200, 180))
        exit_game_rect = exit_game.get_rect(center=(200, 220))
        self.screen.blit(reset, reset_rect)
        self.screen.blit(menu, menu_rect)
        self.screen.blit(exit_game, exit_game_rect)