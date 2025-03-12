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

bg_far_speed = 1  # Far background moves slower
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
RED = (255, 0, 0)

# Dot properties
dot_x = 100
dot_y = 500
velocity = 0
gravity = 0.5
jump_strength = -10
ground_level = 500
jumps_left = 2  # Define jumps_left to keep track of jumps

# Obstacle properties
num_obstacles = 4  # Number of obstacles
obstacles = []

for i in range(num_obstacles):
    x = WIDTH + i * 300  # Spread them out
    y = ground_level
    obstacle_image = random.choice(obstacle_images)  # Choose random image
    obstacle_rect = pygame.Rect(x, y - obstacle_image.get_height(), obstacle_image.get_width(),
                                obstacle_image.get_height())
    obs_mask = pygame.mask.from_surface(obstacle_image)

    obstacles.append([x, y, obstacle_image, obstacle_rect, obs_mask])

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
highscore = 0
score_font = pygame.font.Font("font.TTF", 30)  # Define the font for score
score_text = score_font.render(f"Score: {score}", True, BLACK)  # Black color for score
high_score_text = score_font.render(f"Highscore: {highscore}", True, BLACK)  # Black color for score

# Display intro text for 3 seconds
screen.fill((0, 0, 0))  # Fill the screen with black (clear screen)
screen.blit(intro_text, (WIDTH // 2 - intro_text.get_width() // 2, HEIGHT // 2 - intro_text.get_height() // 2))
pygame.display.flip()  # Update the screen to show the text
pygame.time.delay(3000)  # Wait for 3 seconds (intro screen duration)

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
        obstacles[i][3] = obstacles[i][3].move(-obstacle_speed, 0)

        if obstacles[i][0] < -40:
            obstacles[i][0] = WIDTH + random.randint(150, 200)
            obstacles[i][2] = random.choice(obstacle_images)
            obstacles[i][3] = pygame.Rect(obstacles[i][0], obstacles[i][1] - obstacles[i][2].get_height(), obstacles[i][2].get_width(),
                                          obstacles[i][2].get_height())

            score += 1
            if score > highscore:
                highscore = score

    # Collision detection
    dot_rect = pygame.Rect(dot_x, dot_y - dot_image.get_height(), dot_image.get_width(), dot_image.get_height())

    for obs in obstacles:
        if dot_rect.colliderect(obs[3]):
            score = 0  # Reset score on collision
            #for i in range(num_obstacles):
            #    obstacles[i][0] = WIDTH + i * 200
            #    obstacles[i][2] = random.choice(obstacle_images)

    # for obs in obstacles:
    #    if dot_x <= obs[0] <= dot_x + 40 and dot_y-30 <= obs[1] <= dot_y+30:
    #        score = 0
    #        for i in range(num_obstacles):
    #            obstacles[i][0] = WIDTH + i * 200
    #            obstacles[i][2] = random.choice(obstacle_images)

    # Draw the scrolling background layers
    screen.blit(bg_far, (bg_far_x1, 0))
    screen.blit(bg_far, (bg_far_x2, 0))
    screen.blit(bg_near, (bg_near_x1, 0))
    screen.blit(bg_near, (bg_near_x2, 0))

    # Draw the dot
    screen.blit(dot_image, (dot_x, dot_y - dot_image.get_height()))

    # Draw bugfix
    pygame.draw.rect(screen, RED, dot_rect, width=5)
    pygame.draw.rect(screen, RED, obstacles[0][3], width=5)
    pygame.draw.rect(screen, RED, obstacles[1][3], width=5)
    pygame.draw.rect(screen, RED, obstacles[2][3], width=5)
    pygame.draw.rect(screen, RED, obstacles[3][3], width=5)

    # Draw obstacles
    for obs in obstacles:
        screen.blit(obs[2], (obs[0], obs[1] - obs[2].get_height()))

    # Draw the score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    high_score_text = score_font.render(f"Highscore: {highscore}", True, WHITE)
    screen.blit(high_score_text, (10, 50))

    # Update the display and set the frame rate
    pygame.display.flip()
    clock.tick(60)  # Control the frame rate (60 FPS)

pygame.quit()
