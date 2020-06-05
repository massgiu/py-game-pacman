import pygame, sys
from src.settings import *
from src.player import *
from src.enemy import *
import copy

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.cell_width = MAZE_WIDTH // NUM_COLS
        self.cell_height = MAZE_HEIGHT // NUM_ROWS
        self.walls = []
        self.coins = []
        self.enemies = []
        self.enemies_start_pos = []
        self.player_start_pos, self.enemies_start_pos = self.load()  # load background and init pos
        self.player = Player(self, vec(self.player_start_pos))
        self.make_enemies(self.enemies_start_pos)

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
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
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
            pygame.draw.line(self.background, GREY, (self.cell_width * x, 0), (self.cell_width * x, HEIGHT))
        # horizontal lines
        for y in range(WIDTH // self.cell_height):
            pygame.draw.line(self.background, GREY, (0, self.cell_height * y), (WIDTH, self.cell_height * y))
        # draw lane
        # for coin in self.coins:
        #     pygame.draw.rect(self.background, YELLOW,
        #                      (coin[0]*self.cell_width, coin[1]*self.cell_height, self.cell_width, self.cell_height))

    def load(self):
        self.background = pygame.image.load('../media/maze.png')
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        #reading wall.txt file
        enemies_start_pos = []
        with open('../media/wall.txt', 'r') as file:
            for height, line in enumerate(file):
                for width, char in enumerate(line):
                    if char =='1':
                        self.walls.append(vec(width,height))
                    elif char =='C':
                        self.coins.append(vec(width,height))
                    elif char =='P':
                        player_start_pos = [width,height]
                    elif char in ['2','3','4','5']:
                        enemies_start_pos.append([width,height])
                    elif char == 'B':
                        pygame.draw.rect(self.background, BLACK, (width*self.cell_width, height*self.cell_height,
                                                                  self.cell_width, self.cell_height))
        return player_start_pos, enemies_start_pos
    # Start functions

    def make_enemies(self, enemies_pos):
        for index, enemy_pos in enumerate(enemies_pos):
            self.enemies.append(Enemy(self, vec(enemy_pos), index))

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
        if keys[pygame.K_LEFT]:
            self.player.move(LEFT)
        elif keys[pygame.K_RIGHT]:
            self.player.move(RIGHT)
        elif keys[pygame.K_UP]:
            self.player.move(UP)
        elif keys[pygame.K_DOWN]:
            self.player.move(DOWN)

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
            #enemy hit player
            if enemy.grid_pos == self.player.grid_pos:
                self.remove_life(self.player_start_pos, self.enemies_start_pos)

    def playing_draw(self):
        # clock = pygame.time.Clock()
        # clock.tick(10)
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        self.draw_coins()
        self.draw_grid()
        self.draw_text(f'CURRENT SCORE: {self.player.current_score}', self.screen, (60, 0), 18, WHITE, START_FONT, False)
        self.draw_text(f'HIGH SCORE: {0}', self.screen, (WIDTH//2+60, 0), 18, WHITE, START_FONT, False)
        self.player.draw()
        for index, enemy in enumerate(self.enemies):
            enemy.draw(index)
        pygame.display.update()
        # self.coins.pop()

    def draw_coins(self):
        for coin in self.coins:
            pygame.draw.circle(self.screen, (124, 123, 7), (int(coin.x*self.cell_width+self.cell_width//2) + TOP_BOTTOM_BUFFER//2,
                                                          int(coin.y*self.cell_height+self.cell_height//2) + TOP_BOTTOM_BUFFER//2), 5)
    def remove_life(self, player_start_pos, enemies_start_pos):
        self.player.lives -=1
        if (self.player.lives==0):
            self.state = "game over"
        else:
            self.player.grid_pos = vec(player_start_pos)
            #form grid to pixel
            self.player.pix_pos = self.player.get_pix_pos(self.player.grid_pos)
            self.player.direction = NEUTRAL
            for index, enemy in enumerate(self.enemies):
                enemy.grid_pos = vec(enemies_start_pos[index])
                # form grid to pixel
                enemy.pix_pos = enemy.get_pix_pos(enemy.grid_pos)
                enemy.direction = NEUTRAL

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.reset(self.player_start_pos, self.enemies_start_pos)
        elif keys[pygame.K_ESCAPE]:
            self.running = 'False'

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', self.screen, (WIDTH // 2, HEIGHT // 2 - 50), START_TEXT_SIZE, RED,
                       START_FONT, True)
        self.draw_text('Press the SPACE BAR to continue', self.screen, (WIDTH // 2, HEIGHT // 2 - 20), START_TEXT_SIZE, WHITE,
                       START_FONT, True)
        self.draw_text('Press ESCAPE to quit', self.screen, (WIDTH // 2, HEIGHT // 2), START_TEXT_SIZE,
                       WHITE, START_FONT, True)
        pygame.display.update()

    def reset(self, player_start_pos, enemies_start_pos):
        self.player.lives = 3
        self.player.current_score = 0
        self.player.grid_pos = vec(player_start_pos)
        # form grid to pixel
        self.player.pix_pos = self.player.get_pix_pos(self.player.grid_pos)
        self.player.direction = NEUTRAL
        for index, enemy in enumerate(self.enemies):
            enemy.grid_pos = vec(enemies_start_pos[index])
            # form grid to pixel
            enemy.pix_pos = enemy.get_pix_pos(enemy.grid_pos)
            enemy.direction = NEUTRAL
        self.coins = []
        #redraws coins
        with open('../media/wall.txt', 'r') as file:
            for height, line in enumerate(file):
                for width, char in enumerate(line):
                    if char =='C':
                        self.coins.append(vec(width,height))
        self.state = 'playing'
