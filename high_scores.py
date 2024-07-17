import os
import pygame
import json

def high_scores(screen):
    print("Displaying high scores...")  

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BRIGHT_COLOR = (255, 0, 0)  # Use a bright red color for the title

    # Load custom font for the title
    try:
        title_font = pygame.font.Font(os.path.join('fonts', 'custom_font.ttf'), 100)  # Adjust the font size as needed
    except FileNotFoundError:
        print("Custom font not found. Falling back to default font.")
        title_font = pygame.font.Font(None, 100)  # Use a default font if custom font is not found

    small_font = pygame.font.Font(None, 36)

    # Load background image
    try:
        background = pygame.image.load(os.path.join('images', 'background.png'))
        background = pygame.transform.scale(background, (screen.get_width(), screen.get_height()))
        print("Background image loaded successfully")
    except pygame.error as e:
        print(f"Failed to load background image: {e}")
        background = None  # Use a default color if the background image is not found

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

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)

        # Title
        title_text = title_font.render("High Scores", True, BRIGHT_COLOR)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))

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

        # Calculate initial y_offset to vertically center the text block
        total_height = (small_font.get_height() + 10) * len(high_scores_data[:10])
        y_offset = (screen.get_height() - total_height) // 2 + 100  # Adjust the y_offset to move text block down

        # Display high scores
        for rank, score_entry in enumerate(high_scores_data[:10], start=1):
            try:
                score_text = f"{rank}. {score_entry['name']} : {score_entry['score']}"  # Add space around colon for better readability
                score_text_rendered = small_font.render(score_text, True, BLACK)
                screen.blit(score_text_rendered, (screen.get_width() // 2 - score_text_rendered.get_width() // 2, y_offset))
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
