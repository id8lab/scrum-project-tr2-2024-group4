import pygame
import sys
import cv2
import json
import os
from game_screen import run_game
from high_scores import high_scores


# Pygame initialization
pygame.init()

# Initial screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Main Menu")

# Load the video
cap = cv2.VideoCapture('music/Background.mp4')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Score saving function
def save_score(name, score, file_path='high_scores.json'):
    scores = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            scores = json.load(file)

    scores.append({'name': name, 'score': score})
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:10]

    with open(file_path, 'w') as file:
        json.dump(scores, file)
    print("Score saved successfully.")

# Function to draw the main menu
def draw_main_menu():
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (screen_width, screen_height))
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
    screen.blit(frame, (0, 0))

    title_font_size = max(50, min(100, min(screen_width, screen_height) // 6))
    title_font = pygame.font.Font(None, title_font_size)
    title = title_font.render("Main Menu", True, BLACK)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

    button_font_size = max(30, min(50, min(screen_width, screen_height) // 20))
    button_font = pygame.font.Font(None, button_font_size)
    buttons = {
        "Start Game": (screen_width // 2, screen_height // 2 - 100),
        "Settings": (screen_width // 2, screen_height // 2),
        "High Scores": (screen_width // 2, screen_height // 2 + 100),
        "Exit": (screen_width // 2, screen_height // 2 + 200)
    }

    for text, (x, y) in buttons.items():
        button_rect = pygame.Rect(x - 150, y - 25, 300, 50)
        pygame.draw.rect(screen, GREY, button_rect)
        button_text = button_font.render(text, True, BLACK)
        screen.blit(button_text, (x - button_text.get_width() // 2, y - button_text.get_height() // 2))

def check_button_click(position):
    buttons = {
        "Start Game": (screen_width // 2, screen_height // 2 - 100),
        "Settings": (screen_width // 2, screen_height // 2),
        "High Scores": (screen_width // 2, screen_height // 2 + 100),
        "Exit": (screen_width // 2, screen_height // 2 + 200)
    }
    for text, (x, y) in buttons.items():
        button_rect = pygame.Rect(x - 150, y - 25, 300, 50)
        if button_rect.collidepoint(position):
            return text
    return None

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            button_clicked = check_button_click(event.pos)
            if button_clicked == "Start Game":
                run_game(screen)  # Make sure to save scores within run_game
            elif button_clicked == "Settings":
                setting(screen)
            elif button_clicked == "High Scores":
                high_scores(screen)
            elif button_clicked == "Exit":
                running = False
        elif event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            draw_main_menu()

    draw_main_menu()
    pygame.display.flip()

cap.release()
pygame.quit()
sys.exit()
