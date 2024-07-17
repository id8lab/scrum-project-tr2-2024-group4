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

<<<<<<< HEAD
    # File paths
    scores_file = 'scores.json'

    # Load high scores from a JSON file
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

    # Sort high scores by score in descending order
    high_scores_data.sort(key=lambda x: x['score'], reverse=True)

=======
>>>>>>> bf2001f9d4d4d5f7716dcbbd74804e8f8d76871e
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

<<<<<<< HEAD
        # Determine maximum width of score texts
        max_width = 0
        for score_entry in high_scores_data[:10]:
            try:
                score_text = f"{score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                text_width, _ = small_font.size(score_text)
                if text_width > max_width:
                    max_width = text_width
            except KeyError as e:
                print(f"Error: Missing key {e} in score entry {score_entry}")

        # Display high scores
        y_offset = 150
        for rank, score_entry in enumerate(high_scores_data[:10], start=1):
            try:
                score_text = f"{rank}. {score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                score_text_rendered = small_font.render(score_text, True, BLACK)
                screen.blit(score_text_rendered, (screen.get_width() // 2 - max_width // 2, y_offset))
                y_offset += score_text_rendered.get_height() + 10  # Adjust vertical spacing here
            except KeyError as e:
                print(f"Error: Missing key {e} in score entry {score_entry}")
=======
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
>>>>>>> bf2001f9d4d4d5f7716dcbbd74804e8f8d76871e

        pygame.display.flip()

    return
<<<<<<< HEAD

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    high_scores(screen)
    pygame.quit()
=======
>>>>>>> bf2001f9d4d4d5f7716dcbbd74804e8f8d76871e
