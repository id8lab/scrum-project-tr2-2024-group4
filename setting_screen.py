import pygame

def setting(screen):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 74)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.fill(WHITE)
        game_text = font.render("Setting Screen", True, BLACK)
        screen.blit(game_text, (screen.get_width() // 2 - game_text.get_width() // 2, screen.get_height() // 2 - game_text.get_height() // 2))

        pygame.display.flip()
