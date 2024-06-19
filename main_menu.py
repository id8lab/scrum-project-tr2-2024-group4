import pygame
import sys
import cv2
from game_screen import run_game
from setting_screen import setting
from high_scores import high_scores

# Pygame initialization
pygame.init()

# Initial screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Main Menu")

# Load the video
cap = cv2.VideoCapture('Background.mp4')
try:
    pygame.mixer.music.load('main_menu_music.mp3')
    pygame.mixer.music.set_volume(0.5)  # Volume ranges from 0.0 to 1.0
    pygame.mixer.music.play(-1)  # -1 means loop indefinitely
    print("main menu music loaded and playing")
except pygame.error as e:
    print(f"Failed to load or play main menu music: {e}")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

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
    

    # Dynamic font sizes based on screen dimensions
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

# Function to check button clicks
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
                run_game(screen)
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
