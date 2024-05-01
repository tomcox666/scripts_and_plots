import pygame
from random import randint, uniform
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Particle Explosion Effect")
clock = pygame.time.Clock()

# Particle class with added fading and longer lifespan
class Particle:
    def __init__(self, x, y, color, speed, lifespan, angle):
        self.x = x
        self.y = y
        self.initial_lifespan = lifespan
        self.lifespan = lifespan
        self.color = list(color)  # Make color mutable
        self.speed = speed
        self.radius = 2
        self.angle = angle
        self.fade_rate = uniform(0.005, 0.02)  # Random fade rate for each particle

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifespan -= 1
        self.radius -= 0.01
        self._fade()

    def _fade(self):
        # Reduce color intensity over time to create a fading effect
        fade_ratio = self.lifespan / self.initial_lifespan
        self.color[0] = max(int(self.color[0] * fade_ratio - self.fade_rate), 0)
        self.color[1] = max(int(self.color[1] * fade_ratio - self.fade_rate), 0)
        self.color[2] = max(int(self.color[2] * fade_ratio - self.fade_rate), 0)

    def draw(self, screen):
        pygame.draw.circle(screen, tuple(self.color), (int(self.x), int(self.y)), int(self.radius))

    def is_alive(self):
        return self.lifespan > 0 and self.radius > 0


# Function to create particles
def create_particles(x, y, intensity):
    particles = []
    for _ in range(intensity):
        angle = uniform(0, 2 * math.pi)
        speed = uniform(1, 5)
        lifespan = randint(500, 1000)  # Longer lifespan for particles
        color = (randint(128, 255), randint(128, 255), randint(128, 255))
        p = Particle(x, y, color, speed, lifespan, angle)
        particles.append(p)
    return particles 


# Create a list to hold all active particles
all_particles = []

# Game loop with persistent particles and rapid click response
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Create new particles and add them to the list
            new_particles = create_particles(mouse_x, mouse_y, 80)
            all_particles.extend(new_particles)

    # Clear the screen
    screen.fill(BLACK)

    # Update and draw all active particles
    all_particles = [p for p in all_particles if p.is_alive()]  # Keep only alive particles
    for particle in all_particles:
        particle.update()
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
