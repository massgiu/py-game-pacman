import pygame, sys
from src.settings import *
from src.player import *
from src.enemy import *
from src.utils import *

pygame.init()
vec = pygame.math.Vector2


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'start'
        self.enemies = []
        self.init()

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

    def init(self):
        self.walls, self.coins, self.player_start_pos, self.enemies_start_pos = self.load()  # load background and init pos
        self.player = Player(self, vec(self.player_start_pos)) #grid_pos
        self.make_enemies(self.enemies_start_pos) #grid_pos

    def load(self):
        self.background = pygame.image.load(BACKGROUND_IMG_URL)
        self.background = pygame.transform.scale(self.background, (MAZE_WIDTH, MAZE_HEIGHT))
        walls, coins, player_start_pos, enemies_start_pos = Utils.read_layout(self.background)
        return walls, coins, player_start_pos, enemies_start_pos

    def make_enemies(self, enemies_pos):
        for index, enemy_pos in enumerate(enemies_pos):
            self.enemies.append(Enemy(self, vec(enemy_pos), index))

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
        Utils.draw_text('PUSH SPACE START', self.screen, (WIDTH // 2, HEIGHT // 2 - 50), START_TEXT_SIZE, OCHER,
                       START_FONT, True)
        Utils.draw_text('1 PLAYER ONLY', self.screen, (WIDTH // 2, HEIGHT // 2 + 50), START_TEXT_SIZE, LIGHT_BLUE,
                       START_FONT, True)
        Utils.draw_text('HIGH SCORE', self.screen, (4, 0), START_TEXT_SIZE, WHITE, START_FONT)
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
            # enemy hit player
            if enemy.grid_pos == self.player.grid_pos:
                self.state = Utils.remove_life(self.player, self.player_start_pos, self.enemies, self.enemies_start_pos)

    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2))
        Utils.draw_coins(self.screen, self.coins)
        # Utils.draw_grid(self.background)
        Utils.draw_text(f'CURRENT SCORE: {self.player.current_score}', self.screen, (60, 0), 18, WHITE, START_FONT,
                       False)
        Utils.draw_text(f'HIGH SCORE: {0}', self.screen, (WIDTH // 2 + 60, 0), 18, WHITE, START_FONT, False)
        self.player.draw()
        for index, enemy in enumerate(self.enemies):
            enemy.draw(index)
        pygame.display.update()

    # Game Over functions

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state, self.coins = Utils.reset(self.player, self.enemies, self.player_start_pos,
                                                 self.enemies_start_pos, self.screen)
        elif keys[pygame.K_ESCAPE]:
            self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        Utils.draw_text('GAME OVER', self.screen, (WIDTH // 2, HEIGHT // 2 - 50), START_TEXT_SIZE, RED,
                       START_FONT, True)
        Utils.draw_text('Press the SPACE BAR to continue', self.screen, (WIDTH // 2, HEIGHT // 2 - 20), START_TEXT_SIZE,
                       WHITE, START_FONT, True)
        Utils.draw_text('Press ESCAPE to quit', self.screen, (WIDTH // 2, HEIGHT // 2), START_TEXT_SIZE,
                       WHITE, START_FONT, True)
        pygame.display.update()

    # def reset(self, player_start_pos, enemies_start_pos):
    #     self.player.lives = 3
    #     self.player.current_score = 0
    #     self.player.grid_pos = vec(player_start_pos)
    #     # form grid to pixel
    #     self.player.pix_pos = self.player.from_grid_to_pix_pos(self.player.grid_pos)
    #     self.player.direction = NEUTRAL
    #     for index, enemy in enumerate(self.enemies):
    #         enemy.grid_pos = vec(enemies_start_pos[index])
    #         # form grid to pixel
    #         enemy.pix_pos = enemy.from_grid_to_pix_pos(enemy.grid_pos)
    #         enemy.direction = NEUTRAL
    #     self.coins = []
    #     # redraws coins
    #     _, self.coins, _, _ = Utils.read_layout(self.screen)
    #     self.state = 'playing'
