from PPM import PPM
from ArithmeticCodingCompress import  ArithmeticCodingCompress

class PPM_compressor(PPM):
    def __init__(self, order):
        super().__init__(order)  # Вызов конструктора базового класса
        self.ac_compressor = None

    def encode_symbol(self, context, symbol):
        # len(context), а не self.order, потому что контекст может быть меньше, например для первого символа
        for n in range(len(context), -1, -1):
            encoded_symbol, left, right, total = self.get_probability(context, symbol)
            if (left, right, total) != (0, 0, 0):
                self.ac_compressor.encode_symbol(left / total, (left + right) / total)

                # print(f"symbol: {encoded_symbol} :", left, right, total)

                if encoded_symbol != self.escape:
                    return left, right, total
            context = context[1::] # уменьшаем ебучий контекст

        # это порядок -1, возвращаем, считая что все символы равновероятные
        cum_freq_under = self.get_cum_freq_under(self.contexts[-1], symbol)

        # print(f"symbol: {symbol} :", cum_freq_under, self.contexts[-1][symbol], self.symbols_cnt)
        self.ac_compressor.encode_symbol(cum_freq_under / self.symbols_cnt, (cum_freq_under + self.contexts[-1][symbol]) / self.symbols_cnt)
        return cum_freq_under, self.contexts[-1][symbol], self.symbols_cnt


    def encode_data(self, data):
        self.ac_compressor = ArithmeticCodingCompress(len(data))
        self.symbols_cnt, symbols_set  = self.get_diffrent_symbols_cnt(data)
        self.init_context(symbols_set)
        # print(self.contexts)
        context = ""
        for symbol in data:
            self.encode_symbol(context, symbol)
            self.update_model(context, symbol)
            # print(self.contexts)
            context = (context + symbol)[-self.order:]

        # print(self.ac.end_encode()[:100:])
        return self.ac_compressor.end_encode()


if __name__ == "__main__":
    # data = "alomohora-ahoromola-arohomola-alohomor"
    # data = "abracadabra"
    # data = "abra"
    # import sys
    # sys.stdout = open("debug_compress_info.txt", "w")
    data = "Run-length Encoding is a simple yet effective form of lossless data compression. The basic idea behind RLE is to represent consecutive identical elements, called a “run” in a data stream by a single value and its count rather than as the original run. This is particularly useful when dealing with repetitive sequences, as it significantly reduces the amount of space needed to store or transmit the data."
    ppm = PPM_compressor(4)
    ppm.encode_data(data)
