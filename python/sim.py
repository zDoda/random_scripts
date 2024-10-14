import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 480, 640
BALL_RADIUS = 20
MAX_BALLS = 40
SPHERE_RADIUS = 200
FPS = 240
GRAVITY = 0.5  # Gravitational acceleration
DAMPING = 1    # Energy loss upon collision (1 for elastic collision)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball in Sphere with Opening and Ball Collisions")

# Define some colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Initialize the background color
background_color = BLACK

# Set up the sphere position
sphere_x, sphere_y = WIDTH // 2, HEIGHT // 2

# Define the opening in the circle
opening_angle = random.uniform(0, 2 * math.pi)  # Random angle between 0 and 2π
opening_width = math.radians(30)  # Opening width of 30 degrees converted to radians

# For drawing, calculate start and end angles for the arcs
start_angle_1 = opening_angle + opening_width / 2
end_angle_1 = opening_angle - opening_width / 2 + 2 * math.pi  # Ensure positive angle

# Normalize angles between 0 and 2π
start_angle_1 %= 2 * math.pi
end_angle_1 %= 2 * math.pi

# Define the Ball class
class Ball:
    def __init__(self, x, y, vx, vy, color, is_specific=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.bounce_count = 0
        self.is_specific = is_specific  # Indicates if this ball is the specific one

    def update(self):
        # Apply gravity to the vertical velocity
        self.vy += GRAVITY

        # Move the ball based on its velocity
        self.x += self.vx
        self.y += self.vy

        # Check for collisions with the sphere
        dx = self.x - sphere_x
        dy = self.y - sphere_y
        distance_from_center = math.hypot(dx, dy)

        # Calculate the angle of the ball relative to the center
        ball_angle = math.atan2(-dy, dx)  # Negative dy because Pygame's y-axis is inverted
        ball_angle %= 2 * math.pi  # Normalize angle between 0 and 2π

        # Determine if the ball is within the opening angle
        angle_diff = (ball_angle - opening_angle + 2 * math.pi) % (2 * math.pi)
        in_opening = angle_diff <= opening_width / 2 or angle_diff >= (2 * math.pi - opening_width / 2)

        if distance_from_center >= SPHERE_RADIUS - BALL_RADIUS and not in_opening:
            # Compute the normal vector
            n_x = dx / distance_from_center
            n_y = dy / distance_from_center
            # Compute the dot product of the velocity and normal
            dot = self.vx * n_x + self.vy * n_y
            # Reflect the velocity vector and apply damping
            self.vx = (self.vx - 2 * dot * n_x) * DAMPING
            self.vy = (self.vy - 2 * dot * n_y) * DAMPING
            # Adjust the ball's position
            overlap = distance_from_center - (SPHERE_RADIUS - BALL_RADIUS)
            self.x -= overlap * n_x
            self.y -= overlap * n_y
            # Increment the bounce count
            self.bounce_count += 1

        # Remove the ball if it goes off-screen (after exiting through the opening)
        if (self.x < -BALL_RADIUS or self.x > WIDTH + BALL_RADIUS) or (self.y < -BALL_RADIUS or self.y > HEIGHT + BALL_RADIUS):
            if self in balls:
                balls.remove(self)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), BALL_RADIUS)

# Initialize the list of balls
balls = []

# Create the initial ball (specific ball)
initial_ball = Ball(
    x=WIDTH // 2,
    y=HEIGHT // 2 - 100,  # Start above the center
    vx=5,
    vy=0,
    color=(255, 0, 0),    # Red color
    is_specific=True      # This is the specific ball
)
balls.append(initial_ball)

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all balls
    for ball in balls:
        ball.update()

    # Collision detection between balls
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]
            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y
            distance = math.hypot(dx, dy)
            if distance < 2 * BALL_RADIUS:
                # Collision detected, compute the normal and tangent vectors
                nx = dx / distance
                ny = dy / distance

                # Relative velocity
                dvx = ball1.vx - ball2.vx
                dvy = ball1.vy - ball2.vy

                # Dot product of relative velocity and normal vector
                vn = dvx * nx + dvy * ny

                # If balls are moving towards each other
                if vn > 0:
                    continue

                # Compute impulse scalar
                impulse = -2 * vn / 2  # Divided by sum of inverse masses (1/m + 1/m) with m=1

                # Apply impulse to the velocities
                ball1.vx += impulse * nx
                ball1.vy += impulse * ny
                ball2.vx -= impulse * nx
                ball2.vy -= impulse * ny

                # Adjust positions to prevent overlap
                overlap = 2 * BALL_RADIUS - distance
                ball1.x -= overlap / 2 * nx
                ball1.y -= overlap / 2 * ny
                ball2.x += overlap / 2 * nx
                ball2.y += overlap / 2 * ny

    # Update and draw all balls
    screen.fill(background_color)

    # Draw the sphere with an opening
    rect = pygame.Rect(sphere_x - SPHERE_RADIUS, sphere_y - SPHERE_RADIUS, SPHERE_RADIUS * 2, SPHERE_RADIUS * 2)
    # Draw first arc
    pygame.draw.arc(screen, GREEN, rect, start_angle_1, end_angle_1, 2)

    # Draw second arc if opening doesn't split the circle into one arc
    if end_angle_1 < start_angle_1:
        pygame.draw.arc(screen, GREEN, rect, 0, end_angle_1, 2)
        pygame.draw.arc(screen, GREEN, rect, start_angle_1, 2 * math.pi, 2)

    # Make a copy of the list to avoid modification during iteration
    balls_copy = balls.copy()
    for ball in balls_copy:
        ball.draw(screen)
        # Check if the ball has bounced 4 times
        if ball.bounce_count >= 4:
            # Reset the bounce count
            ball.bounce_count = 0
            # Generate a new random color
            new_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            # Create a new ball with random initial velocity
            if len(balls) < MAX_BALLS:
                new_ball = Ball(
                    x=WIDTH // 2,
                    y=HEIGHT // 2 - 100,  # Start above the center
                    vx=random.uniform(-5, 5),
                    vy=random.uniform(-5, 0),
                    color=new_color
                )
                new_ball.bounce_count = 0
                balls.append(new_ball)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
