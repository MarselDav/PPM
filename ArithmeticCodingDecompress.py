import math

from ArithmeticCoding import ArithmeticCoding


class ArithmeticCodingDecompress(ArithmeticCoding):
    def __init__(self, order):
        super().__init__(order)  # Вызов конструктора базового класса
        self.bit_stream_str = ""
        self.TAG = 0
        self.curr_symbol_ind = 0

    def init_decoding(self, compressed_data, bit_cnt_added_to_last_byte):
        bit_stream_str = []
        for symbol_ind in range(len(compressed_data)):
            symbol = compressed_data[symbol_ind]
            bit_symbol = bin(symbol)[2:].zfill(8)
            for k in range(0, 8):
                bit_stream_str.append(bit_symbol[k])

        bit_stream_str = "".join(bit_stream_str)[:-bit_cnt_added_to_last_byte:]

        self.bit_stream_str = bit_stream_str

        self.TAG = int(self.bit_stream_str[:self.bitlen], 2)

        self.curr_symbol_ind = self.bitlen


    def decode_symbol(self, freq_dict: dict) -> str:
        cum_sum = 0
        cum_list = [0]
        TOTAL_CUM = 0  # !total cumulitive frequency

        freq_dict_sorted = {key : freq_dict[key] for key in sorted(freq_dict.keys())}

        for key in freq_dict_sorted.keys():
            cum_sum += freq_dict_sorted[key]

            TOTAL_CUM += freq_dict_sorted[key]
            cum_list.append(cum_sum)

        freq_reverse_dict = {i: key for i, key in enumerate(freq_dict_sorted.keys())}

        # ----------------
        k = 0
        val = math.floor(((self.TAG - self.left + 1) * TOTAL_CUM - 1) / (self.right - self.left + 1))
        # print("dec: ", cum_list, TOTAL_CUM, val)
        while val >= cum_list[k]:
            k += 1

        decoded_symbol = freq_reverse_dict[k - 1]
        # print(f"symbol: {decoded_symbol} :", cum_list[k - 1], cum_list[k] - cum_list[k - 1], TOTAL_CUM)
        # print(decoded_symbol)

        lenght = self.right - self.left + 1
        left_freq = cum_list[k - 1] / TOTAL_CUM
        righ_freq = cum_list[k] / TOTAL_CUM
        self.left, self.right = self.left + math.floor(lenght * left_freq), self.left + math.floor(lenght * righ_freq) - 1

        while (self.left >= self.max_len / 2 or self.right <= self.max_len / 2 or (
                self.max_len / 4 <= self.left < self.max_len / 2 < self.right <= 3 * self.max_len / 4)) and self.curr_symbol_ind < len(
            self.bit_stream_str) - 1:

            if self.left >= self.max_len / 2 or self.right <= self.max_len / 2:
                self.left = int(bin(self.left)[2:].zfill(self.bitlen)[1:] + '0', 2)  # ? shift left by 1; LSB = 0
                self.right = int(bin(self.right)[2:].zfill(self.bitlen)[1:] + '1', 2)  # ? shift left by 1; LSB = 1
                self.TAG = int(bin(self.TAG)[2:].zfill(self.bitlen)[1:] + self.bit_stream_str[self.curr_symbol_ind], 2)

                binary = bin(self.TAG)[2:].zfill(self.bitlen)[1:]
                self.curr_symbol_ind += 1

            if self.max_len / 4 <= self.left < self.max_len / 2 < self.right <= 3 * self.max_len / 4:
                binary = bin(self.left)[2:].zfill(self.bitlen)[1:]
                self.left = int(str(int(not int(binary[0]))) + binary[1:] + '0',
                           2)  # ? shift left by 1; inverse MSB; LSB = 0
                binary = bin(self.right)[2:].zfill(self.bitlen)[1:]
                self.right = int(str(int(not int(binary[0]))) + binary[1:] + '1',
                            2)  # ? shift left by 1; inverse MSB; LSB = 1

                binary = bin(self.TAG)[2:].zfill(self.bitlen)[1:]

                self.TAG = int(str(int(not int(binary[0]))) + binary[1:] + self.bit_stream_str[self.curr_symbol_ind], 2)

                self.curr_symbol_ind += 1

        return decoded_symbol

