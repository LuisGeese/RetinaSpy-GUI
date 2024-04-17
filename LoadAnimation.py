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

# Eye properties
iris_radius = 30
pupil_radius = 15
eye_x, eye_y = WIDTH - iris_radius - 10, HEIGHT // 2
eye_speed_x, eye_speed_y = 3, 0
blue_eye_moving_out = False  # New flag to control the blue eye's continuous movement

# Brown eye properties
brown_eye_x, brown_eye_y = WIDTH, 0
brown_eye_speed_x, brown_eye_speed_y = -3, 3
brown_eye_on_screen = False
brown_eye_moving = False
brown_eye_wall_hits = 0  # Counter for brown eye touching the right wall


# Timer for introducing brown eye
pygame.time.set_timer(pygame.USEREVENT, 5000)

# Load font
font_path = os.path.join(os.path.dirname(__file__), 'BlackOpsOne-Regular.ttf')
font = pygame.font.Font("C:/Users/Frogs/Downloads/Black_Ops_One/BlackOpsOne-Regular.ttf", 30)

# Render text
text = font.render("RESULTS INCOMING...", True, BLACK)
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 50))

def draw_eye(x, y, color):
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
            brown_eye_on_screen = True

    # Clear the screen
    window.fill(WHITE)

    # Draw blue eye
    draw_eye(eye_x, eye_y, BLUE)

    if brown_eye_on_screen:
        draw_eye(brown_eye_x, brown_eye_y, BROWN)
        if not brown_eye_moving:
            brown_eye_x += brown_eye_speed_x
            brown_eye_y += brown_eye_speed_y
            if brown_eye_y >= eye_y - iris_radius:
                brown_eye_moving = True
                brown_eye_y = eye_y
                eye_speed_x = -5
                eye_speed_y = 5
                blue_eye_moving_out = True  # Trigger continuous movement for blue eye

        if brown_eye_moving:
            brown_eye_x += brown_eye_speed_x
            if brown_eye_x <= iris_radius or brown_eye_x >= WIDTH - iris_radius:
                brown_eye_speed_x *= -1

    if not blue_eye_moving_out:  # Only allow direction change if the blue eye is not moving out
        eye_x += eye_speed_x
        eye_y += eye_speed_y
        if eye_x >= WIDTH - iris_radius or eye_x <= iris_radius:
            eye_speed_x *= -1
        if eye_y >= HEIGHT - iris_radius or eye_y <= iris_radius:
            eye_speed_y *= -1
    else:  # If the blue eye is moving out, it ignores walls
        eye_x += eye_speed_x
        eye_y += eye_speed_y

        if brown_eye_x >= WIDTH - iris_radius:
            brown_eye_wall_hits += 1
            if brown_eye_wall_hits == 2:
                # Trigger the blue eye's new entrance phase after the second touch
                blue_eye_entering = True
                eye_x, eye_y = 0, 0  # Starting position for the blue eye
                eye_speed_x, eye_speed_y = 3, 3  # Diagonal movement towards the right

    window.blit(text, text_rect)

    pygame.display.update()

    clock.tick(60)
