import pygame
import random
import face_tracking

# Initialize face tracker
face_tracker = face_tracking.FaceTracker()

# Initialize pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
BALL_SIZE = 20
BALL_SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ball Game")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Define ball properties
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = random.choice([-BALL_SPEED, BALL_SPEED])
ball_dy = random.choice([-BALL_SPEED, BALL_SPEED])

# Set up the clock
clock = pygame.time.Clock()
FPS = 30

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get face position
    face_y, _ = face_tracker.get_face_position_and_frame()
    if face_y is not None:
        ball_y = face_y

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for collision with screen edges
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_SIZE:
        ball_dx = -ball_dx
    if ball_y <= 0 or ball_y >= SCREEN_HEIGHT - BALL_SIZE:
        ball_dy = -ball_dy

    # Fill the screen with white color
    screen.fill(WHITE)

    # Draw the ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_SIZE)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Clean up
face_tracker.release()
pygame.quit()
