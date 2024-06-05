import pygame
import sys

# Initialize Pygame
pygame.init()

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

# Game loop
running = True
while running:
    for event in pygame.event.get():
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

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()