import pygame
import math
import sys

# Screen dimensions optimized for mobile size
WIDTH, HEIGHT = 350, 600
FPS = 60

# Camera parameters: position and rotation (in degrees)
camera_pos = [0, 0, -5]
camera_rot = [0, 0, 0]  # pitch (x), yaw (y), roll (z)

# Cube definition: vertices in 3D space
cube_vertices = [
    [-1, -1, -1],
    [-1, -1,  1],
    [-1,  1, -1],
    [-1,  1,  1],
    [ 1, -1, -1],
    [ 1, -1,  1],
    [ 1,  1, -1],
    [ 1,  1,  1],
]

# Cube edges connecting vertices by indices
cube_edges = [
    (0,1), (1,3), (3,2), (2,0),  # left face
    (4,5), (5,7), (7,6), (6,4),  # right face
    (0,4), (1,5), (2,6), (3,7)   # connections between faces
]

# Cube faces (optional, could be used for filling or depth sorting)
cube_faces = [
    (0,1,3,2),
    (4,5,7,6),
    (0,1,5,4),
    (2,3,7,6),
    (0,2,6,4),
    (1,3,7,5),
]

def rotate_x(point, angle):
    """Rotate point around X axis by angle in radians"""
    x, y, z = point
    cos_ang = math.cos(angle)
    sin_ang = math.sin(angle)
    y_new = y * cos_ang - z * sin_ang
    z_new = y * sin_ang + z * cos_ang
    return (x, y_new, z_new)

def rotate_y(point, angle):
    """Rotate point around Y axis by angle in radians"""
    x, y, z = point
    cos_ang = math.cos(angle)
    sin_ang = math.sin(angle)
    z_new = z * cos_ang - x * sin_ang
    x_new = z * sin_ang + x * cos_ang
    return (x_new, y, z_new)

def rotate_z(point, angle):
    """Rotate point around Z axis by angle in radians"""
    x, y, z = point
    cos_ang = math.cos(angle)
    sin_ang = math.sin(angle)
    x_new = x * cos_ang - y * sin_ang
    y_new = x * sin_ang + y * cos_ang
    return (x_new, y_new, z)

def project_point(point, width, height, fov, viewer_distance):
    """Project 3D point to 2D using perspective projection"""
    x, y, z = point
    if z + viewer_distance == 0:
        z += 0.0001  # prevent division by zero
    factor = fov / (z + viewer_distance)
    x_proj = x * factor + width / 2
    y_proj = -y * factor + height / 2  # Invert y for pygame coordinate system
    return (int(x_proj), int(y_proj))

def transform_point(point, cam_pos, cam_rot):
    """Apply camera transformations: translate and rotate the point"""
    # Translate point based on camera position (camera moves opposite direction)
    x, y, z = point
    x -= cam_pos[0]
    y -= cam_pos[1]
    z -= cam_pos[2]

    # Rotate around X, then Y, then Z (order matters)
    x, y, z = rotate_x((x, y, z), math.radians(cam_rot[0]))
    x, y, z = rotate_y((x, y, z), math.radians(cam_rot[1]))
    x, y, z = rotate_z((x, y, z), math.radians(cam_rot[2]))

    return (x, y, z)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Cube Projection with Pygame")
    clock = pygame.time.Clock()

    # Field of View and viewer distance for projection
    fov = 256
    viewer_distance = 4

    # For demonstration, rotate the cube over time
    angle_x, angle_y, angle_z = 0, 0, 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((30, 30, 30))  # Dark background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rotate camera around cube (or just rotate cube)
        angle_x += 1
        angle_y += 1
        angle_z += 1

        # Build rotated points array after applying camera transform and cube rotation
        transformed_points = []
        for vertex in cube_vertices:
            # Rotate self for visual effect on cube using angle
            rotated = rotate_x(vertex, math.radians(angle_x))
            rotated = rotate_y(rotated, math.radians(angle_y))
            rotated = rotate_z(rotated, math.radians(angle_z))
            # Then transform by camera position and rotation
            camera_transformed = transform_point(rotated, camera_pos, camera_rot)
            transformed_points.append(camera_transformed)

        # Project the 3D points to 2D screen coordinates
        projected_points = []
        for point in transformed_points:
            proj = project_point(point, WIDTH, HEIGHT, fov, viewer_distance)
            projected_points.append(proj)

        # Draw the edges of the cube
        edge_color = (0, 200, 255)
        edge_width = 2
        for edge in cube_edges:
            start, end = edge
            pygame.draw.line(screen, edge_color, projected_points[start], projected_points[end], edge_width)

        # Optionally draw vertices as small circles and faces with transparency
        vertex_color = (200, 100, 255)
        for p in projected_points:
            pygame.draw.circle(screen, vertex_color, p, 4)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

