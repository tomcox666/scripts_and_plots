import time
import random
import tracemalloc

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.head = None
        self.num_elements = 0

    def push(self, value):
        new_node = Node(value)
        # if stack is empty
        if self.head is None:
            self.head = new_node
        else:
            new_node.next = self.head # place the new node at the head (top) of the linked list
            self.head = new_node

        self.num_elements += 1

    def pop(self):
        if self.is_empty():
            return None
        value = self.head.value # copy data to a local variable
        self.head = self.head.next # move head pointer to next node (top is removed by doing so)
        self.num_elements -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.head.value

    def size(self):
        return self.num_elements

    def is_empty(self):
        return self.num_elements == 0

# Stress test function
def stress_test(stack, num_operations):
    start_time = time.time()
    tracemalloc.start()

    for _ in range(num_operations):
        operation = random.choice(['push', 'pop'])
        if operation == 'push':
            stack.push(random.randint(1, 100))
        elif operation == 'pop':
            stack.pop()

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Execution Time: {end_time - start_time} seconds")
    print(f"Memory Usage: {current / 10**6}MB")
    print(f"Peak Memory Usage: {peak / 10**6}MB")

# Testing the Stack class
stack = Stack()
num_operations = 10000000
stress_test(stack, num_operations)