def decode_message(filename):
    with open(filename, 'r') as f:
        num_word_pairs = [line.strip().split() for line in f]

    triangle_numbers = []
    for num, _ in num_word_pairs:
        if is_triangle_number(int(num)):
            triangle_numbers.append(num)

    num_word_pairs.sort(key=lambda x: int(x[0])) 
    decoded_message = ' '.join([word for num, word in num_word_pairs if num in triangle_numbers])

    return decoded_message

def is_triangle_number(n):
    return ((8 * n + 1)**0.5 - 1) % 2 == 0

if __name__ == "__main__":
    file_path = 'message_file.txt'
    out = decode_message(file_path)
    print(out)
