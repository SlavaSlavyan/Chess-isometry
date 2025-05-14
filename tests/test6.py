import pygame
import sys

def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Semi-transparent Polygon Demo")

    clock = pygame.time.Clock()

    # Define polygon points
    points = [(100, 100), (300, 50), (350, 200), (150, 250)]

    # Create a transparent Surface with per-pixel alpha
    polygon_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # Fill polygon_surface with transparent color (not strictly necessary)
    polygon_surface.fill((0, 0, 0, 0))

    # Define color with alpha (here 128 = 50% transparency)
    color = (255, 0, 0, 128)

    # Draw polygon onto the transparent surface
    pygame.draw.polygon(polygon_surface, color, points)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))  # Fill background white

        # Blit the polygon_surface onto the main screen
        screen.blit(polygon_surface, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

