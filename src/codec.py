import heapq
from collections import defaultdict
from PIL import Image
import numpy as np
from bitarray import bitarray
import pickle
import io
from hashlib import sha256
from Crypto.Cipher import AES

class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freqs):
    heap = [Node(symbol=s, freq=f) for s, f in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(freq=n1.freq + n2.freq)
        merged.left, merged.right = n1, n2
        heapq.heappush(heap, merged)
    return heap[0]

def get_code_lengths(node, path='', lengths=None):
    if lengths is None:
        lengths = {}
    if node.symbol is not None:
        lengths[node.symbol] = len(path)
    else:
        get_code_lengths(node.left, path + '0', lengths)
        get_code_lengths(node.right, path + '1', lengths)
    return lengths

def generate_canonical_codes(code_lengths):
    sorted_symbols = sorted(code_lengths.items(), key=lambda x: (x[1], x[0]))
    codes = {}
    code = 0
    prev_len = 0
    for symbol, length in sorted_symbols:
        code <<= (length - prev_len)
        prev_len = length
        codes[symbol] = format(code, f'0{length}b')
        code += 1
    return codes

def encode_image(img_array, codes):
    bits = bitarray()
    for pixel in img_array.flatten():
        bits.extend(codes[pixel])
    return bits

def decode_bitstream(bitstream, codes, shape):
    rev_map = {v: k for k, v in codes.items()}
    decoded = []
    buffer = ''
    for bit in bitstream.to01():  # convert to '010101...' string
        buffer += bit
        if buffer in rev_map:
            decoded.append(rev_map[buffer])
            buffer = ''
    return np.array(decoded, dtype=np.uint8).reshape(shape)


# =======================
# Main Compression Logic
# =======================

def compress_image(image):
    img = Image.open(image).convert('L')
    img_array = np.array(img)
    freqs = defaultdict(int)
    for val in img_array.flatten():
        freqs[val] += 1

    tree = build_huffman_tree(freqs)
    code_lengths = get_code_lengths(tree)
    codes = generate_canonical_codes(code_lengths)
    bitstream = encode_image(img_array, codes)
    compressed = io.BytesIO()
    pickle.dump((bitstream, code_lengths, img_array.shape), compressed)
    return compressed.getvalue()

def decompress_image(compressed):
    bitstream, code_lengths, shape = pickle.load(compressed)
    codes = generate_canonical_codes(code_lengths)
    img_array = decode_bitstream(bitstream, codes, shape)
    img = Image.fromarray(img_array, mode='L')
    return img

passphrase="chibify"
def get_key(passphrase: str) -> bytes:
    return sha256(passphrase.encode('utf-8')).digest()

def encrypt(data: bytes, passphrase: str) -> bytes:
    key = get_key(passphrase)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    encrypted = cipher.nonce + tag + ciphertext
    return encrypted

def decrypt(encrypted: bytes, passphrase: str) -> bytes:
    key = get_key(passphrase)
    nonce = encrypted[:16]
    tag = encrypted[16:32]
    ciphertext = encrypted[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data
