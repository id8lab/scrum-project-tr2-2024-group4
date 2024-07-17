import pygame
import sys
import random
import math
import json
import os
# Function to get text input from player
def get_text_input(screen, prompt, position):
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(position[0], position[1], 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True  # 开始时输入框为活跃状态
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True  # 按下 Enter 键结束输入
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(prompt + text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    return text


# Function definition
def run_game(screen):
    pygame.init()
    # Game variables
    rect_width, rect_height = 100, 100
    rect_speed = 5
    
    # Load enemy images
    try:
        enemy_images = [pygame.image.load('images/enemy1.png'), pygame.image.load('images/enemy2.png')]
        enemy_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in enemy_images]
        print("Enemy images loaded successfully")
    except pygame.error as e:
        print(f"Failed to load enemy images: {e}")
        sys.exit()

    # Load flight image for the player
    try:
        flight_image = pygame.image.load('images/flight.png')
        flight_image = pygame.transform.scale(flight_image, (rect_width, rect_height))
        print("Flight image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load flight image: {e}")
        sys.exit()

    # Load background music
    try:
        pygame.mixer.music.load('music/background_music.mp3')
        pygame.mixer.music.set_volume(0.5)  # Volume ranges from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        print("Background music loaded and playing")
    except pygame.error as e:
        print(f"Failed to load or play background music: {e}")

    try:
        hit_sound = pygame.mixer.Sound('music/shooting.mp3')
        hit_sound.set_volume(0.5)  # Volume ranges from 0.0 to 1.0
        print("Hit sound loaded successfully")
    except pygame.error as e:
        print(f"Failed to load hit sound: {e}")
        sys.exit()

    # Load heart image for lives
    try:
        heart_image = pygame.image.load('images/heart.png')
        heart_image = pygame.transform.scale(heart_image, (30, 30))  # Adjust the size of the heart image
        print("Heart image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load heart image: {e}")
        sys.exit()

    # Load boss image
    try:
        boss_image = pygame.image.load('images/boss2.png')
        boss_image = pygame.transform.scale(boss_image, (rect_width * 2, rect_height * 2))  # Boss is larger
        print("Boss image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load boss image: {e}")
        sys.exit()

    # Boss class
    class Boss(pygame.sprite.Sprite):
        def __init__(self, image, move_speed=20):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()
            self.rect.x = screen.get_width() // 2 - self.rect.width // 2
            self.rect.y = 50
            self.health = 100
            self.bullets = []
            self.bullet_speed = 8  # Adjust bullet speed as needed
            self.last_shot_time = pygame.time.get_ticks()
            self.shoot_interval = 1000  # Adjust shoot interval to 1 second
            self.shoot_timer = 0
            self.move_speed = move_speed  # Boss movement speed
            self.attack_start_time = pygame.time.get_ticks()
            self.attack_duration = 15000  # Boss appears for 15 seconds
            self.attack_patterns = [self.shoot_straight, self.shoot_spread, self.shoot_diagonal, self.shoot_homing]
            self.current_pattern = 0

        def update(self):
            # Boss behavior here (e.g., move left and right)
            self.rect.x += random.choice([-self.move_speed, self.move_speed])
            if self.rect.right >= screen.get_width() or self.rect.left <= 0:
                self.rect.x -= random.choice([-self.move_speed, self.move_speed])

            # Update boss bullets
            for bullet in self.bullets:
                bullet[1] += bullet[2]  # bullet[2] contains bullet speed in y direction
                bullet[0] += bullet[3]  # bullet[3] contains bullet speed in x direction
                if bullet[1] > screen.get_height() or bullet[0] < 0 or bullet[0] > screen.get_width():
                    self.bullets.remove(bullet)

            # Check shoot timer and interval
            elapsed_time = pygame.time.get_ticks() - self.last_shot_time
            self.shoot_timer += elapsed_time
            self.last_shot_time = pygame.time.get_ticks()

            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                self.attack_patterns[self.current_pattern]()
                self.current_pattern = (self.current_pattern + 1) % len(self.attack_patterns)

        def draw(self, screen):
            screen.blit(self.image, self.rect.topleft)
            # Draw boss bullets
            for bullet in self.bullets:
                pygame.draw.circle(screen, (255, 0, 0), (int(bullet[0]), int(bullet[1])), 5)

        def shoot_straight(self):
            for i in range(8):
                bullet_pos = [self.rect.x + self.rect.width // 2 + i * 10 - 40, self.rect.y + self.rect.height]
                self.bullets.append([bullet_pos[0], bullet_pos[1], self.bullet_speed, 0])

        def shoot_spread(self):
            for i in range(8):
                bullet_pos = [self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height]
                angle = -45 + i * 10
                speed_x = self.bullet_speed * math.sin(math.radians(angle))
                speed_y = self.bullet_speed * math.cos(math.radians(angle))
                self.bullets.append([bullet_pos[0], bullet_pos[1], speed_y, speed_x])

        def shoot_diagonal(self):
            angles = [45, 30, -30, -45]
            for angle in angles:
                bullet_pos = [self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height]
                speed_x = self.bullet_speed * math.sin(math.radians(angle))
                speed_y = self.bullet_speed * math.cos(math.radians(angle))
                self.bullets.append([bullet_pos[0], bullet_pos[1], speed_y, speed_x])

        def shoot_homing(self):
            bullet_pos = [self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height]
            player_pos = [rect_x + rect_width // 2, rect_y + rect_height // 2]
            angle = math.atan2(player_pos[1] - bullet_pos[1], player_pos[0] - bullet_pos[0])
            speed_x = self.bullet_speed * math.cos(angle)
            speed_y = self.bullet_speed * math.sin(angle)
            self.bullets.append([bullet_pos[0], bullet_pos[1], speed_y, speed_x])

    # Score, Level, and Life variables
    score = 0
    level = 1
    lives = 10

    # Bullet variables
    bullets = []
    bullet_speed = -10

    # Enemy variables
    enemies = []
    enemy_speed = 1  # Default enemy speed

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    # Game mode
    mode = 'rectangle'  # Start with 'rectangle' mode, change to 'sprite' with 'S' key

    # Function to update enemy speed based on level
    def update_enemy_speed(level):
        nonlocal enemy_speed
        if level in [1, 2]:
            enemy_speed = 1
        elif level in [3, 4]:
            enemy_speed = 2
        elif level in [5, 6]:
            enemy_speed = 3
        elif level in [7, 8]:
            enemy_speed = 4
        elif level in [9, 10]:
            enemy_speed = 5

    # Game loop
    running = True
    boss = None
    boss_spawn_time = None
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
        if len(enemies) < 5:  # Spawn enemies if fewer than 5
            enemy_x = random.randint(0, screen.get_width() - rect_width)
            enemy_y = random.randint(-100, -40)
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
                        update_enemy_speed(level)  # Update enemy speed when level changes
                    hit_sound.play()

        # Check for player-enemy collisions
        player_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], rect_width, rect_height)
            if player_rect.colliderect(enemy_rect):
                lives -= 1
                enemies.remove(enemy)

        # Spawn boss at level 5
        if level == 5 and boss is None:
            boss = Boss(boss_image)
            boss_spawn_time = pygame.time.get_ticks()

        # Update and draw boss if present
        if boss:
            boss.update()
            boss.draw(screen)

            # Check for bullet-boss collisions
            boss_rect = boss.rect
            for bullet in bullets:
                if boss_rect.collidepoint(bullet):
                    bullets.remove(bullet)
                    boss.health -= 10
                    hit_sound.play()
                    if boss.health <= 0:
                        boss = None
                        score += 500  # Reward for defeating boss

            # Check for player-boss bullet collisions
            for bullet in boss.bullets:
                if player_rect.collidepoint((bullet[0], bullet[1])):
                    boss.bullets.remove(bullet)
                    lives -= 1

            # Remove boss after 15 seconds
            if pygame.time.get_ticks() - boss_spawn_time > boss.attack_duration:
                boss = None

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

            input_box_pos = (screen.get_width() // 2 - 100, screen.get_height() // 2 + 20)
            player_name = get_text_input(screen, "Enter your name: ", input_box_pos)

            final_score = score
            save_score_to_json(player_name, final_score)

            running = False  # Exit the game loop
          
         

        # Update the display
        pygame.display.flip()

        # Frame rate
        pygame.time.Clock().tick(60)

    return final_score  # Return score when game ends



def save_score_to_json(player_name, final_score):
    scores = []
    json_file = 'scores.json'

    # Check if file exists and is not empty
    if os.path.exists(json_file) and os.path.getsize(json_file) > 0:
        with open(json_file, 'r') as f:
            scores = json.load(f)

    scores.append({'name': player_name, 'score': final_score})

    with open(json_file, 'w') as f:
        json.dump(scores, f, indent=4)


# Main code to run the game
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Galaga Arcade 64")
    final_score = run_game(screen)
    print(f"Final Score: {final_score}")
    pygame.quit()