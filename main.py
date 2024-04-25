import sys
import random
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


class Score:
    def __init__(self, screen, game_font):
        self.score = 0
        self.high_score = 0
        self.can_score = True
        self.score_sound_countdown = 100
        self.SCOREEVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SCOREEVENT, 100)
        self.screen = screen
        self.game_font = game_font

    def pipe_score_check(self, pipe_list, score_sound):
        if pipe_list:
            for pipe in pipe_list:
                if 95 < pipe.centerx < 105 and self.can_score:
                    self.score += 1
                    score_sound.play()
                    self.can_score = False
                if pipe.centerx < 0:
                    self.can_score = True

    def update_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

    def score_display(self, game_state, mode, winner="none"):
        if mode == 'Single':
            if game_state == 'main_game':
                score_surface = self.game_font.render(str(int(self.score)), True, (255, 255, 255))
                score_rect = score_surface.get_rect(center=(200, 50))
                self.screen.blit(score_surface, score_rect)
            if game_state == 'game_over':
                score_surface = self.game_font.render(f'Score: {int(self.score)}', True, (255, 255, 255))
                score_rect = score_surface.get_rect(center=(200, 50))
                self.screen.blit(score_surface, score_rect)

                high_score_surface = self.game_font.render(f'High Score: {int(self.high_score)}', True, (255, 255, 255))
                high_score_rect = high_score_surface.get_rect(center=(200, 375))
                self.screen.blit(high_score_surface, high_score_rect)
        elif mode == 'Double':
            if game_state == 'game_over':
                score_surface = self.game_font.render(f'Winner is: {winner}', True, (255, 255, 255))
                score_rect = score_surface.get_rect(center=(200, 50))
                self.screen.blit(score_surface, score_rect)


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


if __name__ == '__main__':
    game = Game()
    game.main_menu()
