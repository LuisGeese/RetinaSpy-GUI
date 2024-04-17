import pygame

# Initialize Pygame
pygame.init()

# Frame dimensions
frame_width, frame_height = 480, 288

# Set up the display
screen = pygame.display.set_mode((frame_width, frame_height))
screen2 = pygame.display.set_mode((frame_width, frame_height), pygame.NOFRAME)
pygame.display.set_caption("SVG Animation")

# Colors
background_color = (0, 0, 0)  # Black

# Function to load and smoothly scale an image
def load_and_smoothly_scale_image(path, target_width, target_height):
    image = pygame.image.load(path)
    width, height = image.get_size()
    scaling_factor = min(target_width / width, target_height / height)
    new_size = (int(width * scaling_factor), int(height * scaling_factor))
    scaled_image = pygame.transform.smoothscale(image, new_size)  # Using smoothscale for better quality
    return scaled_image

# Load and scale your images
logo_5_path = "C:/Users/Frogs/Downloads/Color logo with background (5).svg"
logo_6_path = "C:/Users/Frogs/Downloads/Color logo with background (6).svg"
logo_5 = load_and_smoothly_scale_image(logo_5_path, frame_width * 3.5 // 4, frame_height * 3.5 // 4)
logo_6 = load_and_smoothly_scale_image(logo_6_path, frame_width * 3.5 // 4, frame_height * 3.5 // 4)

# Initial positions for the logos
logo_5_pos = [-logo_5.get_width(), (frame_height - logo_5.get_height()) // 15]  # Start left out of frame
logo_6_pos = [frame_width, (frame_height + logo_5.get_height()) // 2.9]  # Start right out of frame

# Animation parameters
logo_5_target_x = (frame_width - logo_5.get_width()) // 2
logo_6_target_x = (frame_width - logo_6.get_width()) // 2
speed = 0.2  # Reduced speed for smoother, slower movement

# Flag to determine if the animation is complete
animation_complete = False

# Main loop for the animation
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move logo 5 to the center
    if logo_5_pos[0] < logo_5_target_x:
        logo_5_pos[0] += speed
    else:  # Correct overshoot and handle animation completion
        logo_5_pos[0] = logo_5_target_x

    # Move logo 6 to its position below logo 5
    if logo_6_pos[0] > logo_6_target_x:
        logo_6_pos[0] -= speed
    else:  # Correct overshoot and handle animation completion
        logo_6_pos[0] = logo_6_target_x

    # Check if the animation is complete
    if logo_5_pos[0] == logo_5_target_x and logo_6_pos[0] == logo_6_target_x and not animation_complete:
        animation_complete = True
        pygame.time.wait(3000)  # Wait for 2 seconds
        break  # Exit the while loop

    # Clear screen and draw images at their new positions
    screen.fill(background_color)
    screen.blit(logo_5, logo_5_pos)
    screen.blit(logo_6, logo_6_pos)
    pygame.display.flip()

# Quit Pygame
pygame.quit()
