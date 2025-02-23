import pygame
import random

# Initialize Pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jumping Dot")

# Load background images for parallax
bg_far = pygame.image.load("background_far.png")
bg_far = pygame.transform.scale(bg_far, (WIDTH, HEIGHT))

bg_near = pygame.image.load("background_near.png")
bg_near = pygame.transform.scale(bg_near, (WIDTH, HEIGHT))

# Positions for scrolling
bg_far_x1, bg_far_x2 = 0, WIDTH  # Two copies of the far background
bg_near_x1, bg_near_x2 = 0, WIDTH  # Two copies of the near background

bg_far_speed = 1   # Far background moves slower
bg_near_speed = 2  # Near background moves faster

# Load images
dot_image = pygame.image.load("dot.png")  # Your dot image
dot_image = pygame.transform.scale(dot_image, (110, 110))

# Load multiple obstacle images
obstacle_images = [
    pygame.transform.scale(pygame.image.load("obstacle1.png"), (70, 60)),
    pygame.transform.scale(pygame.image.load("obstacle2.png"), (80, 70)),
    pygame.transform.scale(pygame.image.load("obstacle3.png"), (50, 60)),
    pygame.transform.scale(pygame.image.load("obstacle4.png"), (80, 60))
]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Dot properties
dot_x = 100
dot_y = 200
velocity = 0
gravity = 0.5
jump_strength = -10
ground_level = 400
jumps_left = 2  # Define jumps_left to keep track of jumps

# Obstacle properties
num_obstacles = 4  # Number of obstacles
obstacles = []

for i in range(num_obstacles):
    x = WIDTH + i * 300  # Spread them out
    y = ground_level+50
    obstacle_image = random.choice(obstacle_images)  # Choose random image
    obstacles.append([x, y, obstacle_image])

obstacle_speed = 5

# Font setup
try:
    custom_font = pygame.font.Font("font.TTF", 30)  # Replace with your font
    print("Font loaded successfully!")
except Exception as e:
    print(f"Error loading font: {e}")
    custom_font = pygame.font.Font(None, 50)  # Fall back to default font if custom font fails

# Render the intro text using custom font
intro_text = custom_font.render("LEVEL 1: SWEDEN", True, WHITE)

# Score setup
score = 0
score_font = pygame.font.Font("font.TTF", 30)  # Define the font for score
score_text = score_font.render(f"Score: {score}", True, BLACK)  # Black color for score

# Display intro text for 2 seconds
screen.fill((0, 0, 0))  # Fill the screen with black (clear screen)
screen.blit(intro_text, (WIDTH//2 - intro_text.get_width()//2, HEIGHT//2 - intro_text.get_height()//2))
pygame.display.flip()  # Update the screen to show the text
pygame.time.delay(3000)  # Wait for 2 seconds (intro screen duration)

# Game loop
clock = pygame.time.Clock()  # Create clock object for controlling frame rate
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if jumps_left > 0:
                velocity = jump_strength
                jumps_left -= 1

    # Update background positions for parallax effect
    bg_far_x1 -= bg_far_speed
    bg_far_x2 -= bg_far_speed
    bg_near_x1 -= bg_near_speed
    bg_near_x2 -= bg_near_speed

    if bg_far_x1 < -WIDTH:
        bg_far_x1 = WIDTH
    if bg_far_x2 < -WIDTH:
        bg_far_x2 = WIDTH
    if bg_near_x1 < -WIDTH:
        bg_near_x1 = WIDTH
    if bg_near_x2 < -WIDTH:
        bg_near_x2 = WIDTH

    # Gravity effect
    velocity += gravity
    dot_y += velocity

    if dot_y >= ground_level:
        dot_y = ground_level
        velocity = 0
        jumps_left = 2

    # Move obstacles
    for i in range(num_obstacles):
        obstacles[i][0] -= obstacle_speed

        if obstacles[i][0] < -40:
            obstacles[i][0] = WIDTH + random.randint(100, 300)
            obstacles[i][2] = random.choice(obstacle_images)
            score += 1

    # Collision detection
    dot_rect = pygame.Rect(dot_x, dot_y, 30, 30)

    for obs in obstacles:
        obstacle_rect = pygame.Rect(obs[0], obs[1], obs[2].get_width(), obs[2].get_height())
        if dot_rect.colliderect(obstacle_rect):
            score = 0  # Reset score on collision
            for i in range(num_obstacles):
                obstacles[i][0] = WIDTH + i * 200
                obstacles[i][2] = random.choice(obstacle_images)

    # Draw the scrolling background layers
    screen.blit(bg_far, (bg_far_x1, 0))
    screen.blit(bg_far, (bg_far_x2, 0))
    screen.blit(bg_near, (bg_near_x1, 0))
    screen.blit(bg_near, (bg_near_x2, 0))

    # Draw the dot
    screen.blit(dot_image, (dot_x, dot_y))

    # Draw obstacles
    for obs in obstacles:
        screen.blit(obs[2], (obs[0], obs[1]))

    # Draw the score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the display and set the frame rate
    pygame.display.flip()
    clock.tick(60)  # Control the frame rate (60 FPS)

pygame.quit()
