import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("Bouncing Ball with Gravity")

# Create a canvas to draw on
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a ball object
class Ball:
    def __init__(self, x, y, radius, velocity, acceleration=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = velocity
        self.acceleration = acceleration
        self.friction = 0.01  # add friction to slow down the ball

    def move(self):
        # Verlet integration
        self.x_prev = self.x
        self.y_prev = self.y
        self.x += self.velocity[0] * self.dt
        self.y += self.velocity[1] * self.dt
        self.velocity[0] += self.acceleration[0] * self.dt
        self.velocity[1] += self.acceleration[1] * self.dt
        self.velocity[0] *= (1 - self.friction)
        self.velocity[1] *= (1 - self.friction)

        self.drag_force = 0.5 * 0.01 * (self.velocity[0] ** 2 + self.velocity[1] ** 2) * 0.1 * self.radius ** 2
        self.velocity[0] += self.acceleration[0] * self.dt - self.drag_force * self.dt
        self.velocity[1] += self.acceleration[1] * self.dt - self.drag_force * self.dt

        # Bounce off walls and floor
        if self.x <= self.radius or self.x + self.radius >= 400:
            self.velocity[0] = -self.velocity[0]
        if self.y <= self.radius or self.y + self.radius >= 400:
            self.velocity[1] = -self.velocity[1]



    def draw(self, canvas):
        canvas.create_oval(self.x, self.y, self.x + self.radius, self.y + self.radius, fill="#FF0000")

# Create a ball and set its initial position and velocity
ball = Ball(200, 200, 50, [5, 5], acceleration=[0, 0.1])  # add gravity acceleration

# Create a second blue ball
blue_ball = Ball(300, 200, 50, [5, 5], acceleration=[0, 0.1])

# Set up the animation loop
def animate():
    ball.dt = 1  # set time step
    blue_ball.dt = 1
    canvas.delete(tk.ALL)  # Clear everything
    # Optionally redraw background here
    ball.move()
    ball.draw(canvas)
    blue_ball.move()
    blue_ball.draw(canvas)
    root.after(10, animate)  # call animate() again in 10ms

animate()  # start the animation loop

# Run the Tkinter event loop
root.mainloop()