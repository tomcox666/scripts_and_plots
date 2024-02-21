import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

class RNN:
    def __init__(self, input_size, output_size, hidden_size, learning_rate=0.01):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.W_input = np.random.randn(hidden_size, input_size)
        self.W_output = np.random.randn(output_size, hidden_size)
        self.W_hidden = np.random.randn(hidden_size, hidden_size)
        self.learning_rate = learning_rate

    def backward(self, hidden_states, outputs, upstream_gradients):
        d_W_input = np.zeros_like(self.W_input)
        d_W_output = np.zeros_like(self.W_output)
        d_W_hidden = np.zeros_like(self.W_hidden)

        # Backpropagate through time
        for t in reversed(range(len(hidden_states))):
            # Compute gradient for output layer
            d_output = outputs[t] * (1 - outputs[t]) * upstream_gradients[t]
            d_W_output += np.outer(d_output, hidden_states[t])

            # Compute gradient for hidden layer
            d_hidden = np.dot(self.W_output.T, d_output)
            for i in reversed(range(t + 1)):
                d_hidden_total = d_hidden + np.dot(self.W_hidden.T, d_hidden)
                d_hidden = d_hidden_total * hidden_states[i] * (1 - hidden_states[i])
                d_W_hidden += np.outer(d_hidden, hidden_states[i])

                # Compute gradient for input layer
                d_W_input += np.outer(d_hidden, inputs[i])

        # Update weights
        self.W_input -= self.learning_rate * d_W_input
        self.W_output -= self.learning_rate * d_W_output
        self.W_hidden -= self.learning_rate * d_W_hidden

        # Print computed gradients
        print("Gradient for W_input:")
        print(d_W_input)
        print("Gradient for W_output:")
        print(d_W_output)
        print("Gradient for W_hidden:")
        print(d_W_hidden)


# Example usage:
rnn = RNN(input_size=4, output_size=2, hidden_size=3, learning_rate=0.01)
inputs = np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
hidden_states = np.array([[0.1, 0.2, 0.3], [0.2, 0.3, 0.4], [0.3, 0.4, 0.5]])
outputs = np.array([[0.7, 0.8], [0.6, 0.7], [0.5, 0.6]])
upstream_gradients = np.array([[0.1, 0.2], [0.2, 0.3], [0.3, 0.4]])

rnn.backward(hidden_states, outputs, upstream_gradients)