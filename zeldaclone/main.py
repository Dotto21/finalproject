import pygame, sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('img/Arial.ttf', 32)
        
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/TilesetNature.png')
        self.ground_spritesheet = Spritesheet('img/TilesetFloor.png')
        self.attack_spritesheet = Spritesheet('img/Attack.png')
        self.snake_enemy_spritesheet = Spritesheet('img/Snake.png')

    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)  
                if column == "E":
                    SnakeEnemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)
                if column == "T":
                    Chest(self, j, i)

    def new(self):
        # New game starts
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.createTilemap()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.facing == 'idle':
                        Attack(self, self.player.rect.x, self.player.rect.y + 32)
                    if self.player.facing == 'up':
                        Attack(self, self.player.rect.x, self.player.rect.y - 32)
                    if self.player.facing == 'down':
                        Attack(self, self.player.rect.x, self.player.rect.y + 32)
                    if self.player.facing == 'left':
                        Attack(self, self.player.rect.x - 32, self.player.rect.y)
                    if self.player.facing == 'right':
                        Attack(self, self.player.rect.x + 32, self.player.rect.y)

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLUE)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        #game loop
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        title = self.font.render('Final Project', True, BLACK)
        title_rect = title.get_rect(x = 10, y = 10)
        
        play_button = Button(10, 50, 100, 50, WHITE, BLACK, "Play", 32)

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
                
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            
            self.screen.fill(RED)
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

g = Game()
g.intro_screen()
g.new()
while g.running:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()