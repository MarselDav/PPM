import math

class ArithmeticCoding:
    def __init__(self, total_cump):
        self.bitlen = 2 + math.ceil(math.log2(total_cump))
        self.max_len = 2 ** self.bitlen

        self.left = 0
        self.right = self.max_len - 1
        self.bit_stream = []
        self.underflow_count = 0