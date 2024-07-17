import pygame
import json
import os

def high_scores(screen):
    print("Displaying high scores...")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    scores_file = 'high_scores.json'

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        title_text = font.render("High Scores", True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # Check if the file exists and is not empty before attempting to load
        if os.path.exists(scores_file) and os.path.getsize(scores_file) > 0:
            try:
                with open(scores_file, 'r') as f:
                    high_scores_data = json.load(f)
                print(f"Loaded high scores: {high_scores_data}")

                y_offset = 150
                for score_entry in sorted(high_scores_data, key=lambda x: x['score'], reverse=True):
                    score_text = small_font.render(f"{score_entry['name']}: {score_entry['score']}", True, BLACK)
                    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, y_offset))
                    y_offset += 50
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        else:
            print("No scores available or file is empty.")
            no_scores_text = small_font.render("No scores available.", True, BLACK)
            screen.blit(no_scores_text, (screen.get_width() // 2 - no_scores_text.get_width() // 2, 150))

        pygame.display.flip()

    return
