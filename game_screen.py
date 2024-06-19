import pygame
import sys
import random  # Import the random module

# Function definition
def run_game(screen):
    pygame.init()
    # Game variables
    rect_x, rect_y = 50, 50
    rect_width, rect_height = 100, 100
    rect_speed = 5
    sprite_frames = []  # List of surfaces representing different frames
    player_pos = (350, 450)
    current_frame = 0
    frame_count = 0

    # Score, Level, and Life variables
    score = 0
    level = 1
    lives = 3

    # Bullet variables
    bullets = []
    bullet_speed = -10

    # Enemy variables
    enemies = []
    enemy_speed = 5

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    # Game mode
    mode = 'rectangle'  # Start with 'rectangle' mode, change to 'sprite' with 'S' key

    # Game loop
    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    mode = 'sprite' if mode == 'rectangle' else 'rectangle'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    bullet_pos = [rect_x + rect_width // 2, rect_y]
                    bullets.append(bullet_pos)

        # Player control with mouse
        if pygame.mouse.get_focused():
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rect_x = mouse_x - rect_width // 2
            rect_y = mouse_y - rect_height // 2

        # Player control with arrow keys
        if keys[pygame.K_LEFT]:
            rect_x -= rect_speed
        if keys[pygame.K_RIGHT]:
            rect_x += rect_speed
        if keys[pygame.K_UP]:
            rect_y -= rect_speed
        if keys[pygame.K_DOWN]:
            rect_y += rect_speed

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
            # Fill the screen with black
            screen.fill((0, 0, 0))  # Black

            # Draw the rectangle
            pygame.draw.rect(screen, (255, 255, 255), (rect_x, rect_y, rect_width, rect_height))

        # Update bullets
        for bullet in bullets:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, (255, 255, 255), bullet, 5)

        # Update enemies
        if len(enemies) < 5:  # Spawn enemies if fewer than 5
            enemy_x = random.randint(0, screen.get_width() - rect_width)  # Use random.randint
            enemy_y = random.randint(-100, -40)  # Use random.randint
            enemies.append([enemy_x, enemy_y])

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > screen.get_height():
                enemies.remove(enemy)
                lives -= 1

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], rect_width, rect_height))

        # Check for collisions
        for bullet in bullets:
            for enemy in enemies:
                if (enemy[0] < bullet[0] < enemy[0] + rect_width and
                        enemy[1] < bullet[1] < enemy[1] + rect_height):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    if score % 100 == 0:
                        level += 1

        # Display Score, Level, and Lives
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        level_text = font.render(f'Level: {level}', True, (255, 255, 255))
        lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(lives_text, (10, 90))

        # Update the display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)

    return  # Ensure a clean exit

# Main code to run the game
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Galaga Arcade 64")
    run_game(screen)
    pygame.quit()
    sys.exit()
