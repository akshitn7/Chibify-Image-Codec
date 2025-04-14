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


def buildTree(pixelFreq):
    heap = []
    for i in pixelFreq:
        n = Node(i, pixelFreq[i])
        heapq.heappush(heap, n)

    while(len(heap) > 1):
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]


def getCodes(root, code = "", code_book = {}):
    if(root == None):
        return code_book
    if(root.symbol != None):
        code_book[root.symbol] = code
    getCodes(root.left, code + '0', code_book)
    getCodes(root.right, code + '1', code_book)
    return code_book
    
filepath = input("Filepath:")
pixelFreq = fh.getFrequencies(filepath)
root = buildTree(pixelFreq)
huffman_codes = getCodes(root)
print(huffman_codes)