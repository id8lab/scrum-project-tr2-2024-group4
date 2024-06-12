import pygame
import sys
from game_screen import run_game
from setting_screen import setting
from high_scores import high_scores

# Pygame
pygame.init()

# menu screen
screen_width = 1500
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Main Menu")

# define color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# word
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# define buttons
buttons = {
    "Start Game": (screen_width // 2, screen_height // 2 - 100),
    "Settings": (screen_width // 2, screen_height // 2),
    "High Scores": (screen_width // 2, screen_height // 2 + 100),
    "Exit": (screen_width // 2, screen_height // 2 + 200)
}

#loop
running = True

# check
def check_button_click(position):
    for text, (x, y) in buttons.items():
        button_rect = pygame.Rect(x - 150, y - 25, 300, 50)
        if button_rect.collidepoint(position):
            return text
    return None

# Main menu design
def draw_main_menu():
    screen.fill(WHITE)
    title = font.render("Main Menu", True, BLACK)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

    for text, (x, y) in buttons.items():
        pygame.draw.rect(screen, GREY, (x - 150, y - 25, 300, 50))
        button_text = button_font.render(text, True, BLACK)
        screen.blit(button_text, (x - button_text.get_width() // 2, y - button_text.get_height() // 2))

# amin loop
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

    draw_main_menu()
    pygame.display.flip()

pygame.quit()
sys.exit()