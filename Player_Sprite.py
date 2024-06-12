import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors (RGB)
BLACK = (0, 0, 0)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Galaga Arcade 64')

# Clock to control game framerate
clock = pygame.time.Clock()
FPS = 60  # Frames per second

# Load images
player_image = pygame.image.load('Player.png')  # Make sure to provide the correct path to your image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        
        # Keep player within the screen bounds
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

# Sprite group for all sprites
all_sprites = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

def game_loop():
    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update sprite group
        all_sprites.update()

        # Refresh screen
        screen.fill(BLACK)  # Clear screen with black
        all_sprites.draw(screen)  # Draw all sprites

        # Update the display
        pygame.display.flip()

        # Ensure program maintains a rate of 60 frames per second
        clock.tick(FPS)

# Start the game loop
game_loop()
