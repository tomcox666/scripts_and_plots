import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Particle Explosion Simulation with Gravity")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Constants
GRAVITY = 0.1  # Adjust for desired gravitational pull
MASS_THRESHOLD = 3  # Minimum radius for particles to be affected by gravity

# Particle class
class Particle:
    def __init__(self, x, y, radius, color, speed, lifespan):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.lifespan = lifespan
        self.dx = random.uniform(-speed, speed)
        self.dy = random.uniform(-speed, speed)
        self.mass = self.radius * 0.1  # Small mass proportional to size

    def update(self):
        self.x += self.dx
        self.y += self.dy

        # Apply gravity if particle is large enough
        if self.radius >= MASS_THRESHOLD:
            self.dy += GRAVITY * self.mass  

        self.lifespan -= 1

        # Fade the particle over time
        self.color = (self.color[0], self.color[1], self.color[2], int(self.lifespan / 2))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Main simulation loop
def main():
    particles = []
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                create_explosion(pygame.mouse.get_pos())

        # Create an explosion effect on mouse click
        def create_explosion(pos):
            explosion_intensity = 100
            particle_speed = 5
            particle_lifespan = 100
            colors = [RED, YELLOW, WHITE]

            for _ in range(explosion_intensity):
                color = random.choice(colors)
                radius = random.randint(2, 5)
                particles.append(Particle(pos[0], pos[1], radius, color, particle_speed, particle_lifespan))

        # Update and draw particles
        screen.fill(BLACK)
        for particle in particles[:]:  # Work on a copy to avoid mutation issues
            particle.update()
            particle.draw(screen)
            if particle.lifespan <= 0:
                particles.remove(particle)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()