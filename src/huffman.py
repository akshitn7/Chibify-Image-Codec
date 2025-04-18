import heapq
import file_handling as fh
class Node:
    def __init__(self, symbol, freq, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(pixel_freq):
    heap = []
    for i in pixel_freq:
        n = Node(i, pixel_freq[i])
        heapq.heappush(heap, n)

    while(len(heap) > 1):
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def get_codes(root, code = "", code_book = {}):
    if(root == None):
        return code_book
    if(root.symbol != None):
        code_book[root.symbol] = code
    get_codes(root.left, code + '0', code_book)
    get_codes(root.right, code + '1', code_book)
    return code_book

def encode(code_book, pixels):
    bit_string = ""
    for pixel in pixels:
        bit_string += code_book[pixel]
    padding_len = (8 - len(bit_string) % 8) % 8
    padding_info = format(padding_len, "08b")
    final_bit_string = padding_info + bit_string + '0' * padding_len
    byte_array = bytearray()
    for i in range(0, len(final_bit_string), 8):
        chunk = final_bit_string[i:(i+8)]
        byte = int(chunk, 2)
        byte_array.append(byte)
    return byte_array   

def compress(source, destination):
    pixels, shape = fh.get_pixels(source)
    pixel_freq = fh.get_frequencies(pixels)
    root = build_tree(pixel_freq)
    code_book = get_codes(root)
    byte_array = encode(code_book, pixels)
    file_name = input("Enter File Name:")
    destination = destination + "\\" + file_name + ".huff"
    with open (destination, "wb") as dest:
        dest.write(byte_array)