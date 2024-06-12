
import pygame
import sys

# Function definition
def run_game(screen):
    pygame.init()
    # Game variables
    rect_x, rect_y = 50, 50
    rect_width, rect_height = 100, 100
    rect_speed_x, rect_speed_y = 5, 5
    sprite_frames = []  # List of surfaces representing different frames
    player_pos = (350, 450)
    current_frame = 0
    frame_count = 0

    # Game mode
    mode = 'rectangle'  # Start with 'rectangle' mode, change to 'sprite' with 'S' key

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mode = 'sprite' if mode == 'rectangle' else 'rectangle'

        if mode == 'sprite' and sprite_frames:
            # Animation control
            frame_count += 1
            if frame_count >= 10:  # Change frame every 10 game loops
                current_frame = (current_frame + 1) % len(sprite_frames)
                frame_count = 0
            # Draw the current frame
            screen.fill((0, 0, 0))  # Black
            screen.blit(sprite_frames[current_frame], player_pos)
        else:
            # Move the rectangle
            rect_x += rect_speed_x
            rect_y += rect_speed_y

            # Bounce the rectangle off the screen edges
            if rect_x < 0 or rect_x > screen.get_width() - rect_width:
                rect_speed_x = -rect_speed_x
            if rect_y < 0 or rect_y > screen.get_height() - rect_height:
                rect_speed_y = -rect_speed_y

            # Fill the screen with black
            screen.fill((0, 0, 0))  # Black

            # Draw the rectangle
            pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))

        # Update the display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)

    return  # Ensure a clean return after the loop

# Initialization outside the function
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game with Animated Sprite and Rectangle')

# Ensure the game function is only called when needed, not upon import
if __name__ == '__main__':
    run_game(screen)
    pygame.quit()
    sys.exit()
