import pygame
import sys
import random
import math
import json
import os

# Initialize Pygame
pygame.init()

# Function to get text input from player
def get_text_input(screen, prompt, position):
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(0, 0, 140, 32)
    input_box.center = position
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = True
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
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        width = max(200, font.size(prompt + text)[0] + 10)
        input_box.w = width
        input_box.centerx = position[0]

        pygame.draw.rect(screen, color, input_box, 2)
        text_surface = font.render(prompt + text, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        pygame.display.flip()

    return text

# Multiplayer game function
def start_multiplayer_game(screen):
    pygame.init()
    # Game variables
    rect_width, rect_height = 100, 100
    rect_speed = 5

    # Load images
    try:
        flight_image = pygame.image.load('images/flight.png')
        flight_image = pygame.transform.scale(flight_image, (rect_width, rect_height))
    except pygame.error as e:
        print(f"Failed to load flight image: {e}")
        sys.exit()

    try:
        enemy_images = [pygame.image.load('images/enemy1.png'), pygame.image.load('images/enemy2.png')]
        enemy_images = [pygame.transform.scale(img, (rect_width, rect_height)) for img in enemy_images]
    except pygame.error as e:
        print(f"Failed to load enemy images: {e}")
        sys.exit()

    try:
        heart_image = pygame.image.load('images/heart.png')
        heart_image = pygame.transform.scale(heart_image, (30, 30))
    except pygame.error as e:
        print(f"Failed to load heart image: {e}")
        sys.exit()

    # Initialize player positions and scores
    rect1_x, rect1_y = 50, 50
    rect2_x, rect2_y = screen.get_width() - rect_width - 50, screen.get_height() - rect_height - 50
    rect_speed = 5
    player1_name = get_text_input(screen, "Player 1 Name: ", (screen.get_width() // 2, screen.get_height() // 2 - 100))
    player2_name = get_text_input(screen, "Player 2 Name: ", (screen.get_width() // 2, screen.get_height() // 2))

    score1 = 0
    score2 = 0
    lives1 = 3
    lives2 = 3

    # Bullet variables
    bullets1 = []
    bullets2 = []
    bullet_speed = -10

    # Enemy variables
    enemies = []
    enemy_speed = 1

    # Font for displaying text
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    bullet_pos = [rect1_x + rect_width // 2, rect1_y]
                    bullets1.append(bullet_pos)
                elif event.button == 3:  # Right mouse button
                    bullet_pos = [rect2_x + rect_width // 2, rect2_y]
                    bullets2.append(bullet_pos)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            rect1_x -= rect_speed
        if keys[pygame.K_d]:
            rect1_x += rect_speed
        if keys[pygame.K_w]:
            rect1_y -= rect_speed
        if keys[pygame.K_s]:
            rect1_y += rect_speed

        if keys[pygame.K_LEFT]:
            rect2_x -= rect_speed
        if keys[pygame.K_RIGHT]:
            rect2_x += rect_speed
        if keys[pygame.K_UP]:
            rect2_y -= rect_speed
        if keys[pygame.K_DOWN]:
            rect2_y += rect_speed

        screen.fill((0, 0, 0))

        screen.blit(flight_image, (rect1_x, rect1_y))
        screen.blit(flight_image, (rect2_x, rect2_y))

        bullets1 = [bullet for bullet in bullets1 if bullet[1] > 0]
        for bullet in bullets1:
            bullet[1] += bullet_speed
        for bullet in bullets1:
            pygame.draw.circle(screen, (255, 255, 255), bullet, 5)

        bullets2 = [bullet for bullet in bullets2 if bullet[1] > 0]
        for bullet in bullets2:
            bullet[1] += bullet_speed
        for bullet in bullets2:
            pygame.draw.circle(screen, (255, 255, 255), bullet, 5)

        if len(enemies) < 5:
            enemy_x = random.randint(0, screen.get_width() - rect_width)
            enemy_y = random.randint(-100, -40)
            enemy_image = random.choice(enemy_images)
            enemies.append([enemy_x, enemy_y, enemy_image])

        enemies = [enemy for enemy in enemies if enemy[1] <= screen.get_height()]
        for enemy in enemies:
            enemy[1] += enemy_speed
        for enemy in enemies:
            screen.blit(enemy[2], (enemy[0], enemy[1]))

        bullets_to_remove1 = []
        enemies_to_remove = []
        for bullet in bullets1:
            for enemy in enemies:
                if (enemy[0] < bullet[0] < enemy[0] + rect_width and
                        enemy[1] < bullet[1] < enemy[1] + rect_height):
                    bullets_to_remove1.append(bullet)
                    enemies_to_remove.append(enemy)
                    score1 += 10
                    hit_sound.play()

        for bullet in bullets_to_remove1:
            if bullet in bullets1:
                bullets1.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        bullets_to_remove2 = []
        for bullet in bullets2:
            for enemy in enemies:
                if (enemy[0] < bullet[0] < enemy[0] + rect_width and
                        enemy[1] < bullet[1] < enemy[1] + rect_height):
                    bullets_to_remove2.append(bullet)
                    enemies_to_remove.append(enemy)
                    score2 += 10
                    hit_sound.play()

        for bullet in bullets_to_remove2:
            if bullet in bullets2:
                bullets2.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in enemies:
                enemies.remove(enemy)

        screen.blit(font.render(f'Score Player 1: {score1}', True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f'Score Player 2: {score2}', True, (255, 255, 255)), (10, 50))

        for i in range(lives1):
            screen.blit(heart_image, (screen.get_width() - (i + 1) * 40, screen.get_height() - 40))
        for i in range(lives2):
            screen.blit(heart_image, (screen.get_width() - (i + 1) * 40, 20))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
