import networkx as nx
import matplotlib.pyplot as plt

def main():
    print("Welcome to the Random Graph Generator!")

    while True:
        print("\nPlease choose an option:")
        print("1. Generate Erdős–Rényi graph")
        print("2. Generate Barabási–Albert graph")
        print("3. Generate Watts-Strogatz small-world graph")
        print("4. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                nodes = int(input("Enter the number of nodes: "))
                edges = int(input("Enter the number of edges: "))

                if nodes < 1 or edges < 0:
                    raise ValueError

                G = nx.gnm_random_graph(nodes, edges)
                print("Graph generated.")
                visualize(G)

            except ValueError:
                print("Invalid input. Please enter a positive integer for nodes and a non-negative integer for edges.")

        elif choice == "2":
            try:
                nodes = int(input("Enter the number of nodes: "))
                edges = int(input("Enter the number of edges to add at each step: "))

                if nodes < 1 or edges < 1:
                    raise ValueError

                G = nx.barabasi_albert_graph(nodes, edges)
                print("Graph generated.")
                visualize(G)

            except ValueError:
                print("Invalid input. Please enter positive integers for nodes and edges.")

        elif choice == "3":
            try:
                nodes = int(input("Enter the number of nodes: "))
                k = int(input("Enter the number of neighbors for each node: "))
                p = float(input("Enter the probability of rewiring edges (between 0 and 1): "))

                if nodes < 1 or k < 1 or p < 0 or p > 1:
                    raise ValueError

                G = nx.watts_strogatz_graph(nodes, k, p)
                print("Graph generated.")
                visualize(G)

            except ValueError:
                print("Invalid input. Please enter positive integers for nodes and k, and a probability between 0 and 1.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

def visualize(graph):
    while True:
        print("\nPlease choose a visualization option:")
        print("1. Spring layout")
        print("2. Random layout")
        print("3. Circular layout")
        print("4. Save graph as PNG image")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=5000)
            plt.show()

        elif choice == "2":
            pos = nx.random_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=5000)
            plt.show()

        elif choice == "3":
            pos = nx.circular_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=5000)
            plt.show()

        elif choice == "4":
            filename = input("Enter a filename for the PNG image (without .png extension): ")
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=5000)
            plt.savefig(filename + ".png", format="PNG")
            print(f"Graph saved as {filename}.png")
            break

        elif choice == "5":
            print("Returning to main menu.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()