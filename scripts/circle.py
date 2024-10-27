import tkinter as tk
import math
import time

# Constants
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
MIN_VELOCITY_THRESHOLD = 0.01
MATERIALS = {
    "Rubber": 0.9,
    "Steel": 0.7,
    "Wood": 0.6,
    "Plastic": 0.5,
    "Paper": 0.3
}

class Ball:
    def __init__(self, canvas, x, y, angle, velocity, material_factor):
        self.canvas = canvas
        self.radius = 15 
        self.id = self.canvas.create_oval(x - self.radius, y - self.radius, x + self.radius, y + self.radius, fill='blue')
        self.x = x
        self.y = y
        self.angle = math.radians(angle)
        self.velocity_x = velocity * math.cos(self.angle)
        self.velocity_y = -velocity * math.sin(self.angle)
        self.material_factor = material_factor

    def update(self):
        self.velocity_y += GRAVITY
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.velocity_x = -self.velocity_x * self.material_factor
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))

        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.velocity_y = -self.velocity_y * self.material_factor
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

        if abs(self.velocity_y) < MIN_VELOCITY_THRESHOLD:
            self.velocity_y = 0
        if abs(self.velocity_x) < MIN_VELOCITY_THRESHOLD:
            self.velocity_x = 0

        self.canvas.coords(self.id, self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)

class Simulation:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.angle_label = tk.Label(self.master, text="Enter angle (degrees):")
        self.angle_label.pack()
        self.angle_entry = tk.Entry(self.master)
        self.angle_entry.pack()

        self.velocity_label = tk.Label(self.master, text="Enter velocity:")
        self.velocity_label.pack()
        self.velocity_entry = tk.Entry(self.master)
        self.velocity_entry.pack()

        self.material_label = tk.Label(self.master, text="Select material:")
        self.material_label.pack()
        self.material_var = tk.StringVar(self.master)
        self.material_var.set("Rubber")

        self.material_option = tk.OptionMenu(self.master, self.material_var, *MATERIALS.keys())
        self.material_option.pack()

        self.start_button = tk.Button(self.master, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.balls = []
        self.running = False

    def start_simulation(self):
        angle = float(self.angle_entry.get())
        velocity = float(self.velocity_entry.get())
        material_name = self.material_var.get()
        material_factor = MATERIALS[material_name]
        ball = Ball(self.canvas, WIDTH // 2, HEIGHT // 2, angle, velocity, material_factor)
        self.balls.append(ball)

        self.running = True
        self.animate()

    def animate(self):
        if self.running:
            for ball in self.balls:
                ball.update()
            self.master.after(16, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ball Simulation")
    simulation = Simulation(root)
    root.mainloop()