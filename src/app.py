import pygame, sys
from src.settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = WIDTH // 28
        self.cell_height = HEIGHT // 28
        self.load()  # load background

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def draw_text(self, words, screen, pos, size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, color)
        text_size = text.get_size()
        pos = list(pos)  # tuple are immutable, so list conversion
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, tuple(pos))

    def draw_grid(self):
        # vertical lines
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.screen, GREY, (self.cell_width * x, 0), (self.cell_width * x, HEIGHT))
        # horizontal lines
        for y in range(WIDTH // self.cell_height):
            pygame.draw.line(self.screen, GREY, (0, self.cell_height * y), (WIDTH, self.cell_height * y))

    def load(self):
        self.background = pygame.image.load('../media/maze.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    # Start functions

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = 'playing'

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('PUSH SPACE START', self.screen, (WIDTH // 2, HEIGHT // 2 - 50), START_TEXT_SIZE, OCHER,
                       START_FONT, True)
        self.draw_text('1 PLAYER ONLY', self.screen, (WIDTH // 2, HEIGHT // 2 + 50), START_TEXT_SIZE, LIGHT_BLUE,
                       START_FONT, True)
        self.draw_text('HIGH SCORE', self.screen, (4, 0), START_TEXT_SIZE, WHITE, START_FONT)

        pygame.display.update()

    # Playing functions

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()

    def playing_update(self):
        pass

    def playing_draw(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        pygame.display.update()
