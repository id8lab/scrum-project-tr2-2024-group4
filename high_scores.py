import pygame
import json
import os

def interpolate_color(start_color, end_color, factor):
    """Interpolate between two colors. Factor is between 0 and 1."""
    red = start_color[0] + (end_color[0] - start_color[0]) * factor
    green = start_color[1] + (end_color[1] - start_color[1]) * factor
    blue = start_color[2] + (end_color[2] - start_color[2]) * factor
    return (int(red), int(green), int(blue))

def high_scores(screen):
    print("Displaying high scores...")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    # Title font
    title_font = pygame.font.Font(None, 74)
    # Load background image
    background = pygame.image.load('images/background.png')

    scores_file = 'scores.json'
    try:
        if os.path.exists(scores_file):
            with open(scores_file, 'r') as f:
                high_scores_data = json.load(f)
            print(f"Loaded high scores: {high_scores_data}")
        else:
            print(f"File '{scores_file}' not found. Creating a new one.")
            high_scores_data = []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        high_scores_data = []

    high_scores_data.sort(key=lambda x: x['score'], reverse=True)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        screen_width, screen_height = screen.get_size()
        background_scaled = pygame.transform.scale(background, (screen_width, screen_height))

        screen.blit(background_scaled, (0, 0))

        # Title with gradient
        title_text = "High Scores"
        title_position = screen.get_width() // 2 - title_font.size(title_text)[0] // 2
        x_offset = 0
        for i, letter in enumerate(title_text):
            color = interpolate_color(RED, BLUE, i / len(title_text))
            letter_rendered = title_font.render(letter, True, color)
            screen.blit(letter_rendered, (title_position + x_offset, 50))
            x_offset += letter_rendered.get_width()

        # Font sizes for the top 3 ranks
        font_sizes = [60, 50, 40]
        y_offset = 150  # Starting y position for scores
        for rank, score_entry in enumerate(high_scores_data[:3], start=1):
            try:
                rank_font = pygame.font.Font(None, font_sizes[rank-1])
                score_text = f"{rank}. {score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                score_text_rendered = rank_font.render(score_text, True, BLACK)
                
                position = (screen.get_width() // 2 - score_text_rendered.get_width() // 2, y_offset + (rank - 1) * 80)
                screen.blit(score_text_rendered, position)
            except KeyError as e:
                print(f"Error: Missing key {e} in score entry {score_entry}")

        pygame.display.flip()

    return

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    high_scores(screen)
    pygame.quit()