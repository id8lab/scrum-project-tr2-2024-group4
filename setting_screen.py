import pygame

def setting(screen):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREY = (200, 200, 200)

    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    
    music_volume = 0.5  # Initial music volume
    brightness = 0.5  # Initial brightness

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if music_slider_rect.collidepoint(mouse_x, mouse_y):
                    music_volume = (mouse_x - music_slider_rect.x) / music_slider_rect.width
                    pygame.mixer.music.set_volume(music_volume)
                if brightness_slider_rect.collidepoint(mouse_x, mouse_y):
                    brightness = (mouse_x - brightness_slider_rect.x) / brightness_slider_rect.width

        screen.fill([int(255 * brightness)] * 3)

        game_text = font.render("Setting Screen", True, BLACK)
        screen.blit(game_text, (screen.get_width() // 2 - game_text.get_width() // 2, 50))
        
        # Music volume slider
        music_text = small_font.render(f"Music Volume: {int(music_volume * 100)}%", True, BLACK)
        screen.blit(music_text, (100, 200))
        music_slider_rect = pygame.Rect(300, 200, 200, 20)
        pygame.draw.rect(screen, GREY, music_slider_rect)
        pygame.draw.rect(screen, BLACK, music_slider_rect, 2)
        pygame.draw.rect(screen, BLACK, (300, 200, int(200 * music_volume), 20))

        # Brightness slider
        brightness_text = small_font.render(f"Brightness: {int(brightness * 100)}%", True, BLACK)
        screen.blit(brightness_text, (100, 300))
        brightness_slider_rect = pygame.Rect(300, 300, 200, 20)
        pygame.draw.rect(screen, GREY, brightness_slider_rect)
        pygame.draw.rect(screen, BLACK, brightness_slider_rect, 2)
        pygame.draw.rect(screen, BLACK, (300, 300, int(200 * brightness), 20))

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.mixer.music.load("music/main_menu_music.mp3")  # Replace with your actual music file
    pygame.mixer.music.play(-1)  # Play music in a loop
    setting(screen)
    pygame.quit()
