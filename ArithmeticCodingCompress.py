import math
from ArithmeticCoding import ArithmeticCoding


class ArithmeticCodingCompress(ArithmeticCoding):
    def __init__(self, bits_buffer, total_cump):
        super().__init__(total_cump)  # Вызов конструктора базового класса
        self.bits_buffer = bits_buffer

    def encode_symbol(self, left_freq, right_freq):
        lenght = self.right - self.left + 1

        self.left, self.right = self.left + math.floor(lenght * left_freq), self.left + math.floor(lenght * right_freq) - 1

        while self.left >= self.max_len / 2 or self.right <= self.max_len / 2 or (
                self.max_len / 4 <= self.left < self.max_len / 2 < self.right <= 3 * self.max_len / 4):

            if self.left >= self.max_len / 2 or self.right <= self.max_len / 2:

                same_bit = bin(self.left)[2:].zfill(self.bitlen)[0]

                self.left = int(bin(self.left)[2:].zfill(self.bitlen)[1:] + '0', 2)  # ? shift left by 1; LSB = 0

                if self.right < 0:
                    raise Exception("right < 0")

                self.right = int(bin(self.right)[2:].zfill(self.bitlen)[1:] + '1', 2)  # ? shift left by 1; LSB = 1

                self.bits_buffer.add(same_bit)
                self.bit_stream.append(same_bit)
                for _ in range(self.underflow_count):
                    self.bit_stream.append(str(int(not int(same_bit))))
                    self.bits_buffer.add(str(int(not int(same_bit))))

                self.underflow_count = 0

            if self.max_len / 4 <= self.left < self.max_len / 2 < self.right <= 3 * self.max_len / 4:
                self.underflow_count += 1

                binary = bin(self.left)[2:].zfill(self.bitlen)[1:]
                self.left = int(str(int(not int(binary[0]))) + binary[1:] + '0',
                           2)  # ? shift left by 1; inverse MSB; LSB = 0
                binary = bin(self.right)[2:].zfill(self.bitlen)[1:]
                self.right = int(str(int(not int(binary[0]))) + binary[1:] + '1',
                            2)  # ? shift left by 1; inverse MSB; LSB = 1

    def end_encode(self):
        if self.left <= self.max_len / 4:
            self.bit_stream.append('0')
            self.bits_buffer.add("0")
            for _ in range(self.underflow_count + 1):
                self.bit_stream.append('1')
                self.bits_buffer.add("1")
        else:
            self.bit_stream.append('1')
            self.bits_buffer.add("1")
            for _ in range(self.underflow_count + 1):
                self.bit_stream.append('0')
                self.bits_buffer.add("0")

        bytes_len = len(self.bits_buffer.bytes) + 1

        for _ in range(bytes_len * 8 - (len(self.bits_buffer.bytes) + len(self.bits_buffer.current_bin_code))):
            self.bit_stream.append('0')
            self.bits_buffer.add("0")

        return "".join(self.bit_stream)