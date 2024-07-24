import os
import pygame
import json

def high_scores(screen):
<<<<<<< HEAD
    print("Displaying high scores.")  
=======
    print("Displaying high scores...")  
<<<<<<< HEAD
    print("Displaying high scores")  
=======
>>>>>>> c7cb746bf5589a44ffc0a72638a3bbbbb746e7c4
>>>>>>> refs/remotes/origin/main

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    # File paths
    scores_file = 'scores.json'
    # Load background image
    background = pygame.image.load('images/background.png')
    background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
    # Load runner-up image
    runner_up_image = pygame.image.load('images/runner_up.png')
    runner_up_image = pygame.transform.scale(runner_up_image, (400, 300))  # Enlarging the runner_up image

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

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

        screen.blit(background, (0, 0))  # Display the background image

        # Title
        title_text = font.render("High Scores", True, (255, 0, 0))
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

        # Display the runner-up image
        screen.blit(runner_up_image, (screen.get_width() // 2 - runner_up_image.get_width() // 2, 150))

        # Display high scores
        y_offset = 320
        for rank, score_entry in enumerate(high_scores_data[:10], start=1):
            try:
                if rank == 1:
                    position = (screen.get_width() // 2 - 100, y_offset - 100)
                elif rank == 2:
                    position = (screen.get_width() // 2 - 150, y_offset)
                elif rank == 3:
                    position = (screen.get_width() // 2 + 50, y_offset)
                else:
                    position = (screen.get_width() // 2 - 100, y_offset + 60 + (rank - 4) * 40)

                score_text = f"{rank}. {score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                score_text_rendered = small_font.render(score_text, True, BLACK)
                screen.blit(score_text_rendered, position)
                y_offset += score_text_rendered.get_height() + 10  # Adjust vertical spacing here
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
