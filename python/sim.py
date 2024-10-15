import pygame
import math
import random
import numpy as np  # Import NumPy for array manipulation

# Initialize Pygame and the mixer with specific settings
pygame.init()
freq = 44100     # Audio CD quality
bitsize = -16    # Unsigned 16-bit
channels = 1     # Mono (requested)
buffer = 1024    # Number of samples
pygame.mixer.init(freq, bitsize, channels, buffer)

# Check actual mixer settings
actual_freq, actual_bitsize, actual_channels = pygame.mixer.get_init()
print(f"Mixer initialized with frequency={actual_freq}, bitsize={actual_bitsize}, channels={actual_channels}")

# Set up some constants
WIDTH, HEIGHT = 480, 640
BALL_RADIUS = 20
MAX_BALLS = 25
SPHERE_RADIUS = 200
FPS = 60
GRAVITY = 0.6  # Gravitational acceleration
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

# Function to generate a sound effect
def generate_click_sound():
    duration = 0.1  # seconds
    frequency = 1000  # Hz
    volume = 4096  # Max 32767 for 16-bit audio

    samples = int(duration * freq)
    t = np.linspace(0, duration, samples, False)
    # Generate a damped sine wave (click sound)
    envelope = np.exp(-5 * t)  # Damping envelope
    wave = volume * np.sin(2 * np.pi * frequency * t) * envelope

    # Ensure the wave is in the correct format
    wave = wave.astype(np.int16)
    
    # Get the actual number of mixer channels
    _, _, actual_channels = pygame.mixer.get_init()
    
    # Reshape the wave array to match the mixer channels
    wave = np.tile(wave.reshape(-1, 1), (1, actual_channels))
    
    return pygame.sndarray.make_sound(wave)

# Generate the click sound
bounce_sound = generate_click_sound()

# Set up the sphere position
sphere_x, sphere_y = WIDTH // 2, HEIGHT // 2

# Define the opening in the circle (located in the bottom half)
opening_angle = random.uniform(math.pi / 2, 3 * math.pi / 2)  # Random angle between π/2 and 3π/2
opening_width = math.radians(30)  # Opening width of 30 degrees converted to radians

# For drawing, calculate start and end angles for the arcs
start_angle_1 = (opening_angle + opening_width / 2) % (2 * math.pi)
end_angle_1 = (opening_angle - opening_width / 2) % (2 * math.pi)

# Adjust if the end angle is less than the start angle
if end_angle_1 < start_angle_1:
    end_angle_1 += 2 * math.pi

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
            # Collision with the circle boundary
            # Play the bounce sound
            bounce_sound.play()

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
                # Spawn new balls inside the circle, but only if total number of balls is less than MAX_BALLS
                num_new_balls = min(2, MAX_BALLS - len(balls))
                for _ in range(num_new_balls):
                    # Generate random angle and distance within the circle
                    angle = random.uniform(0, 2 * math.pi)
                    radius = random.uniform(0, SPHERE_RADIUS - BALL_RADIUS)
                    x = sphere_x + radius * math.cos(angle)
                    y = sphere_y - radius * math.sin(angle)  # Minus because of Pygame coordinate system
                    # Generate random velocity
                    vx = random.uniform(-5, 5)
                    vy = random.uniform(-5, 5)
                    # Generate random color
                    new_color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255)
                    )
                    # Create and append the new ball
                    new_ball = Ball(x, y, vx, vy, new_color)
                    balls.append(new_ball)

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
    # Create a copy to prevent index errors if balls are removed
    balls_copy = balls.copy()
    for i in range(len(balls_copy)):
        for j in range(i + 1, len(balls_copy)):
            ball1 = balls_copy[i]
            ball2 = balls_copy[j]
            dx = ball2.x - ball1.x
            dy = ball2.y - ball1.y
            distance = math.hypot(dx, dy)
            if distance < 2 * BALL_RADIUS:
                # Collision detected
                # Play the bounce sound
                bounce_sound.play()

                # Compute normal and tangent vectors
                nx = dx / distance
                ny = dy / distance
                tx = -ny
                ty = nx

                # Project velocities onto normal and tangent vectors
                v1n = ball1.vx * nx + ball1.vy * ny
                v1t = ball1.vx * tx + ball1.vy * ty
                v2n = ball2.vx * nx + ball2.vy * ny
                v2t = ball2.vx * tx + ball2.vy * ty

                # Swap normal velocities (elastic collision)
                v1n_new = v2n
                v2n_new = v1n

                # Compute new velocities
                ball1.vx = v1n_new * nx + v1t * tx
                ball1.vy = v1n_new * ny + v1t * ty
                ball2.vx = v2n_new * nx + v2t * tx
                ball2.vy = v2n_new * ny + v2t * ty

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
    # Draw the circle arc with the opening
    pygame.draw.arc(screen, GREEN, rect, start_angle_1, end_angle_1, 2)

    # If the arc wraps around, draw the remaining part
    if end_angle_1 - start_angle_1 < 2 * math.pi - opening_width:
        pygame.draw.arc(screen, GREEN, rect, end_angle_1, start_angle_1 + 2 * math.pi, 2)

    for ball in balls:
        ball.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
