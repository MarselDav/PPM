from PPM import PPM
from ArithmeticCodingDecompress import ArithmeticCodingDecompress

class PPM_decompressor(PPM):
    def __init__(self, order):
        super().__init__(order)  # Вызов конструктора базового класса
        self.ac_decompressor = None


    def decode_symbol(self, context):
        # len(context), а не self.order, потому что контекст может быть меньше, например для первого символа
        for n in range(len(context), -1, -1):
            if context in self.contexts:
                decode_symbol = self.ac_decompressor.decode_symbol(self.contexts[context])
                if decode_symbol != self.escape:
                    return decode_symbol
            context = context[1::] # уменьшаем ебучий контекст

        decode_symbol = self.ac_decompressor.decode_symbol(self.contexts[-1])
        return decode_symbol


    def decode_data(self, encoded_data, diffrent_symbols, original_data_len):
        self.ac_decompressor = ArithmeticCodingDecompress(original_data_len)
        self.ac_decompressor.init_decoding(encoded_data)
        self.init_context(diffrent_symbols)
        decode_data = ""
        context = ""
        # print(self.contexts)
        while len(decode_data) != original_data_len:
            decode_symbol = self.decode_symbol(context)
            decode_data += decode_symbol
            self.update_model(context, decode_symbol)
            # print(self.contexts)
            context = (context + decode_symbol)[-self.order:]

        return decode_data


if __name__ == "__main__":
    # data = "alomohora-ahoromola-arohomola-alohomor"
    # data = "abracadabra"
    # data = "Run-length Encoding is a simple yet effective form of lossless data compression. The basic idea behind RLE is to represent consecutive identical elements, called a “run” in a data stream by a single value and its count rather than as the original run. This is particularly useful when dealing with repetitive sequences, as it significantly reduces the amount of space needed to store or transmit the data."
    ppm = PPM_decompressor(4)
    # ppm.encode_data(data)