import pygame
import math
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Parameters for the grid
rows, cols = 8, 8
spacing = 50
grid_offset_x = -175 * spacing  # from original code, but negative large offset makes circles too far left,
# so adjust to center visually
# Let's recalculate grid offsets so the grid is centered and square.

# Calculate total width and height of grid
grid_width = (cols - 1) * spacing
grid_height = (rows - 1) * spacing

center_x = width // 2
center_y = height // 2

rotate = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Increase rotate angle
    rotate += 0.01  # radians

    for y in range(rows):
        for x in range(cols):
            # Calculate original position of circle relative to grid center
            offset_x = x * spacing - grid_width / 2
            offset_y = y * spacing - grid_height / 2

            # Rotate point by rotate angle
            rotated_x = offset_x * math.cos(rotate) - offset_y * math.sin(rotate)
            rotated_y = offset_x * math.sin(rotate) + offset_y * math.cos(rotate)

            # Calculate final screen position
            draw_x = int(center_x + rotated_x)
            draw_y = int(center_y + rotated_y)

            # Draw circle
            pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), 5, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

