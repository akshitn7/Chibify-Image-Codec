import file_handling as fh
import huffman as huff

filepath_src = r"D:\Git Repos\Huffman-Image-Codec\tests\inputs\7.jpg"
filepath_dest = r"D:\Git Repos\Huffman-Image-Codec\tests\outputs"
huff.compress(filepath_src, filepath_dest)