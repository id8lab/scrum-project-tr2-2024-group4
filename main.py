import pygame
import sys

# Initialize Pygame
pygame.init()

<<<<<<< HEAD
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
=======
# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Game Screen")

# Rectangle properties
rect_width = 100
rect_height = 100
rect_x = screen_width // 2 - rect_width // 2
rect_y = screen_height // 2 - rect_height // 2
rect_speed_x = 5
rect_speed_y = 5
>>>>>>> refs/remotes/origin/main

# Game loop
running = True
while running:
    for event in pygame.event.get():
<<<<<<< HEAD
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
=======
        if event.type == pygame.QUIT:
            running = False

    # Move the rectangle
    rect_x += rect_speed_x
    rect_y += rect_speed_y

    # Bounce the rectangle off the screen edges
    if rect_x < 0 or rect_x > screen_width - rect_width:
        rect_speed_x = -rect_speed_x
    if rect_y < 0 or rect_y > screen_height - rect_height:
        rect_speed_y = -rect_speed_y

    # Fill the screen with black
    screen.fill(black)

    # Draw the rectangle
    pygame.draw.rect(screen, white, (rect_x, rect_y, rect_width, rect_height))
>>>>>>> refs/remotes/origin/main

    # Update the display
    pygame.display.flip()

<<<<<<< HEAD
    # Frame rate
    pygame.time.Clock().tick(60)
=======
    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
>>>>>>> refs/remotes/origin/main
