import pygame

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