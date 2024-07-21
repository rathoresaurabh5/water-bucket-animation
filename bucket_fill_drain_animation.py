import pygame
import numpy as np

# Define colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
BLUE = (50, 150, 255)
WHITE = (255, 255, 255)
# Define screen dimensions
WIDTH = 800
HEIGHT = 600

# Define bucket properties
bucket_base_width = 200
bucket_top_width = bucket_base_width * 3
bucket_height = int(HEIGHT * 0.35)
bucket_thickness = 5
bucket_x = WIDTH // 2
bucket_y = HEIGHT - bucket_height // 2 - 20

# Define water filling properties
water_rise_speed = bucket_height / (20 * 60)  # Fills in 20 seconds at 60 fps

# Define animation durations (in frames)
tilt_duration = int(0.3 * 60)  # 300 ms at 60 fps
pour_duration = int(2 * 60)  # 2 seconds at 60 fps
reset_duration = int(0.3 * 60)  # 300 ms at 60 fps
cycle_duration = 20 * 60 + tilt_duration + pour_duration + reset_duration  # 20 seconds to fill + tilt + pour + reset

# Define bucket vertices
def get_bucket_vertices(x, y, base_width, top_width, height, thickness):
    return [
        (x - base_width // 2, y + height // 2),
        (x + base_width // 2, y + height // 2),
        (x + top_width // 2 - thickness, y - height // 2),
        (x - top_width // 2 + thickness, y - height // 2)
    ]

def tilt_bucket(bucket_vertices, angle):
    """
    Tilts the bucket vertices by a given angle.

    Args:
        bucket_vertices: The vertices of the bucket.
        angle: The angle in radians by which to tilt the bucket.

    Returns:
        The tilted bucket vertices.
    """
    center_x = sum([vertex[0] for vertex in bucket_vertices]) / len(bucket_vertices)
    center_y = sum([vertex[1] for vertex in bucket_vertices]) / len(bucket_vertices)
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)
    tilted_vertices = []
    for vertex in bucket_vertices:
        x, y = vertex
        x -= center_x
        y -= center_y
        x_new = x * cos_angle - y * sin_angle
        y_new = x * sin_angle + y * cos_angle
        x_new += center_x
        y_new += center_y
        tilted_vertices.append((x_new, y_new))
    return tilted_vertices

def draw_tilted_water(screen, bucket_x, bucket_y, bucket_base_width, bucket_top_width, bucket_height, water_level, angle):
    center_x = bucket_x
    center_y = bucket_y
    cos_angle = np.cos(angle)
    sin_angle = np.sin(angle)

    for i in range(int(water_level)):
        current_width = int(bucket_base_width + (bucket_top_width - bucket_base_width) * (i / bucket_height))
        x1 = -current_width // 2
        y1 = bucket_height // 2 - i - 1
        x2 = current_width // 2
        y2 = y1

        x1_rot = x1 * cos_angle - y1 * sin_angle + center_x
        y1_rot = x1 * sin_angle + y1 * cos_angle + center_y
        x2_rot = x2 * cos_angle - y2 * sin_angle + center_x
        y2_rot = x2 * sin_angle + y2 * cos_angle + center_y

        pygame.draw.line(screen, BLUE, (x1_rot, y1_rot), (x2_rot, y2_rot), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Water Bucket Animation")
    clock = pygame.time.Clock()

    water_level = 0  # Initialize water_level here
    running = True
    current_frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update water level
        if current_frame <= 20 * 60:
            water_level = min(water_level + water_rise_speed, bucket_height)
        elif current_frame > (20 * 60 + tilt_duration):
            water_level = max(water_level - bucket_height / pour_duration, 0)

        current_frame += 1
        
        if current_frame >= cycle_duration:
            current_frame = 0
            water_level = 0

        # Clear screen
        screen.fill(WHITE)

        # Draw bucket
        bucket_vertices = get_bucket_vertices(bucket_x, bucket_y, bucket_base_width, bucket_top_width, bucket_height, bucket_thickness)

        if current_frame > 20 * 60 and current_frame <= (20 * 60 + tilt_duration):
            tilt_angle = np.pi / 6 * (current_frame - 20 * 60) / tilt_duration  # Tilt to 30 degrees
            tilted_vertices = tilt_bucket(bucket_vertices, tilt_angle)
        elif current_frame > (20 * 60 + tilt_duration) and current_frame <= (20 * 60 + tilt_duration + pour_duration):
            tilt_angle = np.pi / 6  # Maintain tilt angle
            tilted_vertices = tilt_bucket(bucket_vertices, tilt_angle)
        elif current_frame > (20 * 60 + tilt_duration + pour_duration):
            reset_angle = np.pi / 6 * (1 - (current_frame - (20 * 60 + tilt_duration + pour_duration)) / reset_duration)
            tilted_vertices = tilt_bucket(bucket_vertices, reset_angle)
        else:
            tilted_vertices = bucket_vertices

        pygame.draw.polygon(screen, BLACK, tilted_vertices, bucket_thickness)

        # Draw water
        if current_frame <= 20 * 60:
            for i in range(int(water_level)):
                current_width = int(bucket_base_width + (bucket_top_width - bucket_base_width) * (i / bucket_height))
                water_rect = pygame.Rect(bucket_x - current_width // 2, bucket_y + bucket_height // 2 - i - 1, current_width, 1)
                pygame.draw.rect(screen, BLUE, water_rect)
        elif current_frame > (20 * 60 + tilt_duration):
            draw_tilted_water(screen, bucket_x, bucket_y, bucket_base_width, bucket_top_width, bucket_height, water_level, tilt_angle)

        # Update display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
