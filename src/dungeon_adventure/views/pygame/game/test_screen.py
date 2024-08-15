import pygame


class TestScreen:
    def __init__(self, width: int, height: int, scale_factor: int):
        self.width = width * scale_factor
        self.height = height * scale_factor
        self.surface: pygame.Surface = pygame.Surface((200, 200))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, surface.get_rect().center)


if __name__ == "__main__":
    pygame.init()
    screen_width, screen_height = 800, 600
    pygame_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("UI Test")

    ui_screen = TestScreen()  # Instantiate your Screen class

    # Add some UI elements to your screen for testing
    # For example:
    # ui_screen.add_panel(x=100, y=100, width=200, height=150)
    # ui_screen.add_button(x=150, y=200, width=100, height=50, text="Test Button")

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle other events if needed
            # ui_screen.handle_event(event)

        pygame_screen.fill((255, 255, 255))  # Fill with white background

        # Draw your UI elements
        ui_screen.draw(pygame_screen)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()
