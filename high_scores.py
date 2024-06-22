import pygame
import json

def high_scores(screen):
    print("Displaying high scores...")  

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Load high scores from a JSON file
    try:
        with open('high_scores.json', 'r') as f:
            high_scores_data = json.load(f)
        print(f"Loaded high scores: {high_scores_data}")  
    except FileNotFoundError:
        print("Error: 'high_scores.json' file not found. Creating a new one.")
        high_scores_data = []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        high_scores_data = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)

        # Title
        title_text = font.render("High Scores", True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # Display high scores
        y_offset = 150
        for score_entry in high_scores_data:
            try:
                score_text = small_font.render(f"{score_entry['name']}: {score_entry['score']}", True, BLACK)
                screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, y_offset))
                y_offset += 50
            except KeyError as e:
                print(f"Error: Missing key {e} in score entry {score_entry}")

        pygame.display.flip()

    # Return to main menu
    return
