import heapq
import collections
import os
import pickle

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged_node = HuffmanNode(None, node1.freq + node2.freq)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(heap, merged_node)

    return heap[0]

def build_huffman_codes(root, current_code="", codes={}):
    if root is None:
        return

    if root.char is not None:
        codes[root.char] = current_code
        return

    build_huffman_codes(root.left, current_code + "0", codes)
    build_huffman_codes(root.right, current_code + "1", codes)
    return codes

def compress(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    freq_dict = collections.Counter(text)
    root = build_huffman_tree(freq_dict)
    codes = build_huffman_codes(root)

    encoded_text = "".join(codes[char] for char in text)

    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte_str = encoded_text[i:i+8]
        if len(byte_str) < 8:
            byte_str = byte_str.ljust(8, '0')
        byte_array.append(int(byte_str, 2))

    try:
        with open(output_file, 'wb') as f:
            pickle.dump(root, f)  
            f.write(bytes(byte_array))
        print(f"File compressed to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")

def decompress(input_file, output_file):
    try:
        with open(input_file, 'rb') as f:
            root = pickle.load(f)
            byte_data = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    bit_string = "".join(bin(byte)[2:].zfill(8) for byte in byte_data)

    decoded_text = ""
    current_node = root
    for bit in bit_string:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    try:
        with open(output_file, 'w') as f:
            f.write(decoded_text)
        print(f"File decompressed to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")


if __name__ == "__main__":
    action = input("Choose action (compress/decompress): ")
    input_file = input("Enter input file name: ")
    output_file = input("Enter output file name: ")

    if action == "compress":
        compress(input_file, output_file)
    elif action == "decompress":
        decompress(input_file, output_file)
    else:
        print("Invalid action.")