import pygame
import json
import os

def high_scores(screen):
    print("Displaying high scores...")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    # Load background image
    background = pygame.image.load('images/background.png')
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))

    # Load runner-up image
    runner_up_image = pygame.image.load('images/runner_up.png')
    runner_up_image = pygame.transform.scale(runner_up_image, (400, 300))  # Enlarging the runner_up image

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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.blit(background, (0, 0))

        # Title
        title_text = font.render("High Scores", True, BLACK)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # Display the runner-up image
        screen.blit(runner_up_image, (screen.get_width() // 2 - runner_up_image.get_width() // 2, 150))

        # Display top three high scores with manually adjusted positions
        positions = [
            (screen.get_width() // 2 - 100, 240),  # Adjust this for the first place
            (screen.get_width() // 2 - 200, 290),  # Adjust this for the second place
            (screen.get_width() // 2 + 80, 310)   # Adjust this for the third place
        ]
        
        for rank, (pos, score_entry) in enumerate(zip(positions, high_scores_data[:3]), start=1):
            try:
                score_text = f"{rank}. {score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                score_text_rendered = small_font.render(score_text, True, BLACK)
                screen.blit(score_text_rendered, pos)
            except KeyError as e:
                print(f"Error: Missing key {e} in score entry {score_entry}")

        pygame.display.flip()

    # Return to main menu
    return

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    high_scores(screen)
    pygame.quit()