import pygame
import sys
import random

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

    # Load enemy images
    try:
        enemy_images = [pygame.image.load('enemy1.png'), pygame.image.load('enemy2.png')]
        enemy_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in enemy_images]
        print("Enemy images loaded successfully")
    except pygame.error as e:
        print(f"Failed to load enemy images: {e}")
        sys.exit()

    # Load flight image for the player
    try:
        flight_image = pygame.image.load('flight.png')
        flight_image = pygame.transform.scale(flight_image, (rect_width, rect_height))
        print("Flight image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load flight image: {e}")
        sys.exit()

    # Load background music
    try:
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.set_volume(0.5)  # Volume ranges from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        print("Background music loaded and playing")
    except pygame.error as e:
        print(f"Failed to load or play background music: {e}")

    try:
        hit_sound = pygame.mixer.Sound('shooting.mp3')
        hit_sound.set_volume(0.5)  # Volume ranges from 0.0 to 1.0
        print("Hit sound loaded successfully")
    except pygame.error as e:
        print(f"Failed to load hit sound: {e}")
        sys.exit()

    # Load heart image for lives
    try:
        heart_image = pygame.image.load('heart.png')
        heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust the size of the heart image
        print("Heart image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load heart image: {e}")
        sys.exit()

    # Load boss image
    try:
        boss_image = pygame.image.load('Boss1.png')
        boss_image = pygame.transform.scale(boss_image, (200, 200))  # Adjust the size of the boss image
        print("Boss image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load boss image: {e}")
        sys.exit()

    # Score, Level, and Life variables
    score = 0
    level = 1
    lives = 10

    # Bullet variables
    bullets = []
    bullet_speed = -10

    # Enemy variables
    enemies = []
    enemy_speed = 5

    # Boss variables
    boss = None
    boss_speed = 2
    boss_health = 50
    boss_attacks = []

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

        # Fill the screen with black
        screen.fill((0, 0, 0))  # Black

        # Draw the flight image
        screen.blit(flight_image, (rect_x, rect_y))

        # Update bullets
        for bullet in bullets:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Draw bullets
        for bullet in bullets:
            pygame.draw.circle(screen, (255, 255, 255), bullet, 5)

        # Update enemies
        if boss is None and len(enemies) < 5:  # Spawn enemies if fewer than 5 and no boss
            enemy_x = random.randint(0, screen.get_width() - rect_width)  # Use random.randint
            enemy_y = random.randint(-100, -40)  # Use random.randint
            enemy_image = random.choice(enemy_images)
            enemies.append([enemy_x, enemy_y, enemy_image])

        for enemy in enemies:
            enemy[1] += enemy_speed
            if enemy[1] > screen.get_height():
                enemies.remove(enemy)
                lives -= 1

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy[2], (enemy[0], enemy[1]))

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
                    hit_sound.play()

        # Check for level 10 and spawn boss
        if level == 10 and boss is None:
            enemies.clear()  # Clear all existing enemies
            boss = [screen.get_width() // 2 - 100, -200]  # Start position of the boss

        # Update boss position
        if boss is not None:
            if boss[1] < 50:  # Move boss down until it reaches y = 50
                boss[1] += boss_speed
            screen.blit(boss_image, (boss[0], boss[1]))

            # Boss attack pattern
            if random.randint(0, 50) == 0:  # Randomly fire bullets
                boss_bullet_pos = [boss[0] + boss_image.get_width() // 2, boss[1] + boss_image.get_height()]
                boss_attacks.append(boss_bullet_pos)

            # Update boss bullets
            for attack in boss_attacks:
                attack[1] += -bullet_speed
                if attack[1] > screen.get_height():
                    boss_attacks.remove(attack)

            # Draw boss bullets
            for attack in boss_attacks:
                pygame.draw.circle(screen, (255, 0, 0), attack, 5)

            # Check for collisions between player and boss bullets
            for attack in boss_attacks:
                if (rect_x < attack[0] < rect_x + rect_width and
                        rect_y < attack[1] < rect_y + rect_height):
                    boss_attacks.remove(attack)
                    lives -= 1

            # Check for collisions between player bullets and boss
            for bullet in bullets:
                if (boss[0] < bullet[0] < boss[0] + boss_image.get_width() and
                        boss[1] < bullet[1] < boss[1] + boss_image.get_height()):
                    bullets.remove(bullet)
                    boss_health -= 1

            # Check for boss defeat
            if boss_health <= 0:
                boss = None
                level += 1
                boss_attacks.clear()

        # Display Score and Level
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        level_text = font.render(f'Level: {level}', True, (255, 255, 255))

        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))

        # Display Lives as hearts
        for i in range(lives):
            screen.blit(heart_image, (screen.get_width() - (i + 1) * 40, screen.get_height() - 40))

        # Check for game over
        if lives <= 0:
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 20))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds before quitting
            running = False

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
