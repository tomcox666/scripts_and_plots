import pygame
import random

# Initialize Pygame and sound mixer
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(160)  # Increase the number of available sound channels

# Load sound effects
explosion_sound = pygame.mixer.Sound('explosion.wav')  # Sound for the first explosion
fireworks_sound = pygame.mixer.Sound('explosion_2.mp3')  # Sound for the second explosion

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Particle Explosion Simulation with Energy")

# Colors for different types of explosions
colors_first_explosion = [pygame.Color("red"), pygame.Color("yellow"), pygame.Color("orange"), pygame.Color("white")]
colors_second_explosion = [pygame.Color("blue"), pygame.Color("purple"), pygame.Color("green"), pygame.Color("cyan")]

# Constants
GRAVITY = 0.1  # Gravitational force
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
        self.velocity = (energy / self.mass) ** 0.5  # Correct velocity based on energy
        self.dx = random.uniform(-self.velocity, self.velocity)
        self.dy = random.uniform(-self.velocity, self.velocity)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.dy += GRAVITY  # Gravity effect

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
                if event.button == 1:  # Left-click for the first explosion
                    create_explosion(pygame.mouse.get_pos(), explosion_sound, colors_first_explosion)
                elif event.button == 3:  # Right-click for the second explosion
                    create_explosion(pygame.mouse.get_pos(), fireworks_sound, colors_second_explosion)

        # Create an explosion effect
        def create_explosion(pos, sound, colors):
            explosion_energy = 275000  # Total energy of the explosion
            num_particles = 100  # Number of particles
            particle_energy = explosion_energy / num_particles  # Energy per particle

            # Find an available channel and play the sound
            channel = pygame.mixer.find_channel()
            if channel:
                channel.play(sound)

            for _ in range(num_particles):
                color = random.choice(colors)
                radius = random.randint(2, 5)
                particles.append(Particle(pos[0], pos[1], radius, color, particle_energy))

        # Update and draw particles
        screen.fill((0, 0, 0))  # Fill the screen with black
        particles = [p for p in particles if p.x >= 0 and p.x < screen_width and p.y >= 0 and p.y < screen_height]  # Keep particles in bounds

        for particle in particles:
            particle.update()  # Update particle position
            particle.draw(screen)  # Draw particle on screen

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # Exit Pygame

if __name__ == "__main__":
    main()