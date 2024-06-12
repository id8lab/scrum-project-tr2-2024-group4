import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game with Animated Sprite')

# Define colors
BLACK = (0, 0, 0)

# Load sprite sheet
sprite_sheet_image = pygame.image.load('sprite.png')
sprite_sheet_width = sprite_sheet_image.get_width()
sprite_width, sprite_height = 80, 80  # Size of each sprite frame, adjust these as needed

# Calculate the number of frames based on the image width
num_frames = sprite_sheet_width // sprite_width

# Extract sprite frames
sprite_frames = []
for i in range(num_frames):  # Use the calculated number of frames
    sprite_frames.append(sprite_sheet_image.subsurface((i * sprite_width, 0, sprite_width, sprite_height)))

# Player properties
player_pos = [screen_width // 2, screen_height // 2]
current_frame = 0
frame_count = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Animation control
    frame_count += 1
    if frame_count >= 10:  # Change frame every 10 game loops
        current_frame = (current_frame + 1) % len(sprite_frames)
        frame_count = 0

    # Fill the screen
    screen.fill(BLACK)

    # Draw the current frame
    screen.blit(sprite_frames[current_frame], player_pos)

    # Update the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)
