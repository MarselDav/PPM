from PPM_compressor import PPM_compressor
from PPM_decompressor import PPM_decompressor
import time


if __name__ == "__main__":
     data = """Huffman encoding is a method of compressing strings. The key idea is to replace each character in the string by a sequence of bits in such a way that characters occurring more frequently have a shorter bit representation than characters occurring less frequently. This usually saves space compared to an encoding where all characters are represented by bit sequences of equal length (as, for example, in the standard ASCII encoding). For this, we have to compute the frequencies of all characters and then to organise that information in a binary tree. The tree can then be used for both the encoding and the decoding of the input string. See Wikipedia for a detailed description.

We are going to derive a (simplistic) Maple implementation of the functions needed to encode and to decode strings using Huffman's method. It will provide an example of how custom data structures (in this case binary trees) can be represented and used in Maple.The next step is to turn the frequency sequence into a Huffman tree. Although it is possible to represent trees in Maple by simply using nested lists, we will implement a more advanced method. This will be both more readable and less error-prone. The idea is to introduce data types for nodes and leaves of our trees. We will use an expression of the form Leaf(d) to represent a leaf with data d and we will use Node(l,r) for representing a node with left subtree l and right subtree r.

Maple does not have a formal data type declaration and in fact, we could use the expressions just without further preparations. However, we decide to enable type checking for our trees. This way, we can later easily check whether something is a leaf or node. Also, we can use the types in the argument lists of procedures in order to guard ourselves against wrong input."""

     # start_time = time.time_ns()
     # cnt = 100
     # for i in range(cnt):
     #      ppm_compressor = PPM_compressor(4)
     #      encoded_data = ppm_compressor.encode_data(data)
     #
     #      ppm_decompressor = PPM_decompressor(4)
     #      orig_data = ppm_decompressor.decode_data(encoded_data, ppm_compressor.get_diffrent_symbols_cnt(data)[1],
     #                                               len(data))
     # end_time = time.time_ns()
     # print((end_time - start_time) // cnt)

     # print(bytes(chr(257).encode("utf-8")))

     model_order = 4
     original_text = "test.txt"
     # original_text = "enwik7.txt"
     compressed_text = "compressed.txt"
     decompressed_text = "decompressed.txt"

     with open(original_text, "rb") as file_reader:
          length = len(file_reader.read())

     ppm_compressor = PPM_compressor(model_order)
     ppm_compressor.encode_data(original_text, compressed_text)

     ppm_decompressor = PPM_decompressor(model_order)
     ppm_decompressor.decode_data(length, compressed_text, decompressed_text)

     with open(original_text, "rb") as file_reader:
          original_data = file_reader.read()

     with open(decompressed_text, "rb") as file_reader:
          decompressed_data = file_reader.read()

     print(original_data == decompressed_data)