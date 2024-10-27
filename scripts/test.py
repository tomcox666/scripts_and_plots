                     
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

def figure_to_array(fig):
    """Converts a Matplotlib figure to a NumPy array representing the RGB values.

    Args:
        fig: The Matplotlib figure to convert.

    Returns:
        A NumPy array with shape (height, width, 3), where the last dimension 
        represents RGB values (0-255).
    """
    
    # Associate the figure with a canvas to render it
    canvas = FigureCanvasAgg(fig)
    
    # Render the figure to the canvas (important step!)
    canvas.draw()

    # Get the rendered buffer as an RGBA string
    s = canvas.tostring_rgb() 

    # Convert the string to a NumPy array
    array = np.fromstring(s, dtype=np.uint8, sep='')
    
    # Reshape the array to match the figure's dimensions (height, width, RGB channels)
    array = array.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return array


# --- Example Usage ---

# Create a sample plot
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6])

# Convert the figure to a NumPy array
img_array = figure_to_array(fig)

print(img_array.shape)  # Display the shape of the resulting array
# Output: (Height, Width, 3)

# Close the figure (optional)
plt.close(fig) 
                  