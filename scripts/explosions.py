import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Particle Explosion Simulation with Energy")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Constants
GRAVITY = 0.1  
DENSITY = 1  # Density of the particle material

# Particle class
class Particle:
    def __init__(self, x, y, radius, color, energy):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.energy = energy
        self.volume = (4/3) * 3.14159 * radius**3
        self.mass = self.volume * DENSITY
        self.velocity = (energy / self.mass) ** 0.5  # Square root for correct energy relationship
        self.dx = random.uniform(-self.velocity, self.velocity)
        self.dy = random.uniform(-self.velocity, self.velocity)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY 

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
            explosion_energy = 275000  # Total energy of the explosion
            num_particles = 100 
            colors = [RED, YELLOW, WHITE] 

            particle_energy = explosion_energy / num_particles

            for _ in range(num_particles):
                color = random.choice(colors)
                radius = random.randint(2, 5) 
                particles.append(Particle(pos[0], pos[1], radius, color, particle_energy))

        # Update and draw particles
        screen.fill(BLACK)
        for particle in particles: 
            particle.update()
            particle.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()