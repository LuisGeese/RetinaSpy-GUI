import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
WIDTH, HEIGHT = 480, 288
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eyeball Animation")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BROWN = (165, 42, 42)

# Set up the clock
clock = pygame.time.Clock()

# Brown eye properties (switched roles with blue eye)
brown_eye_radius = 30
brown_eye_pupil_radius = 15
brown_eye_x, brown_eye_y = WIDTH // 5, HEIGHT // 2
brown_eye_speed_x, brown_eye_speed_y = 3, 0  # Move to the right initially
brown_eye_moving_out = False

# Blue eye properties (switched roles with brown eye)
blue_eye_x, blue_eye_y = 0, 0  # Start from the upper left corner
blue_eye_speed_x, blue_eye_speed_y = 3, 3  # Move diagonally down to the right
blue_eye_on_screen = False
blue_eye_moving = False
blue_eye_wall_hits = 0  # Counter for blue eye touching the right wall

# Timer for introducing blue eye
pygame.time.set_timer(pygame.USEREVENT, 4500)

# Load font
font_path = os.path.join(os.path.dirname(__file__), 'BlackOpsOne-Regular.ttf')
font = pygame.font.Font("C:/Users/Frogs/Downloads/Black_Ops_One/BlackOpsOne-Regular.ttf", 30)

# Render text
text = font.render("RESULTS INCOMING...", True, BLACK)
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))

def draw_eye(x, y, color, iris_radius, pupil_radius):
    pygame.draw.circle(window, WHITE, (x, y), iris_radius + 10)
    pygame.draw.circle(window, BLACK, (x, y), iris_radius + 20, 3)
    pygame.draw.circle(window, color, (x, y), iris_radius)
    pygame.draw.circle(window, BLACK, (x, y), pupil_radius)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.USEREVENT:
            blue_eye_on_screen = True

    # Clear the screen
    window.fill(WHITE)

    # Brown eye boundary check and movement
    brown_eye_x += brown_eye_speed_x
    if brown_eye_x <= brown_eye_radius or brown_eye_x >= WIDTH - brown_eye_radius:
        brown_eye_speed_x *= -1  # Reverse direction

    # Draw brown eye
    draw_eye(brown_eye_x, brown_eye_y, BROWN, brown_eye_radius, brown_eye_pupil_radius)

    # Blue eye appearance and movement logic
    if blue_eye_on_screen:
        # Draw blue eye
        draw_eye(blue_eye_x, blue_eye_y, BLUE, brown_eye_radius, brown_eye_pupil_radius)  # Using brown eye's radius sizes for consistency in switch

        # Before colliding with the brown eye, move diagonally
        if not blue_eye_moving:
            blue_eye_x += blue_eye_speed_x
            blue_eye_y += blue_eye_speed_y

            # If blue eye reaches the same height as brown eye, change brown eye movement
            if blue_eye_y >= brown_eye_y - brown_eye_radius:
                blue_eye_moving = True
                blue_eye_y = brown_eye_y
                brown_eye_speed_x, brown_eye_speed_y = 5, 5  # Change brown eye movement
                brown_eye_moving_out = True

        # After collision, blue eye moves left and right within boundaries
        if blue_eye_moving:
            blue_eye_x += blue_eye_speed_x
            # Reverse blue eye direction at boundaries
            if blue_eye_x <= brown_eye_radius or blue_eye_x >= WIDTH - brown_eye_radius:
                blue_eye_speed_x *= -1

    # Display the text
    window.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)
