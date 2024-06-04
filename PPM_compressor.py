import pickle

from PPM import PPM
from ArithmeticCodingCompress import  ArithmeticCodingCompress
from BitsBuffer import BitsBuffer

class PPM_compressor(PPM):
    def __init__(self, order, is_equally_probable=True, exclusion=False, update_exclusion=False):
        super().__init__(order, is_equally_probable, exclusion, update_exclusion)  # Вызов конструктора базового класса
        self.ac_compressor = None

    def encode_symbol(self, context, symbol):
        exclusion_symbols = set()
        for n in range(len(context), -1, -1): # len(context), а не self.order, потому что контекст может быть меньше, например для первого символа
            encoded_symbol, left, right, total = self.get_probability(context, symbol, exclusion_symbols)
            if (left, right, total) != (0, 0, 0):
                self.ac_compressor.encode_symbol(left / total, (left + right) / total)

                # print(f"symbol: {encoded_symbol} :", left, right, total)

                if encoded_symbol != self.escape:
                    return context

                if self.exclusion:
                    exclusion_symbols.update(set(self.contexts[context].keys()))  # добавляем символы в исключения

            context = context[1::] # уменьшаем контекст


        cum_freq_under = self.get_cum_freq_under(self.contexts[-1], symbol) # это порядок -1, возвращаем, считая что все символы равновероятные

        # print(f"symbol: {symbol} :", cum_freq_under, self.contexts[-1][symbol], self.symbols_cnt)
        self.ac_compressor.encode_symbol(cum_freq_under / self.symbols_cnt, (cum_freq_under + self.contexts[-1][symbol]) / self.symbols_cnt)
        return -1


    def encode_data(self, file_input, file_output):
        with open(file_input, "rb") as file_reader:
            file_data = file_reader.read()
            data_len = len(file_data)

            with open(file_output, "wb") as file_writer:
                bits_buffer = BitsBuffer()
                bits_buffer.set_file_writer(file_writer)

                self.ac_compressor = ArithmeticCodingCompress(bits_buffer, data_len)
                self.symbols_cnt, symbols_set  = self.get_diffrent_symbols_cnt(file_data, data_len)

                pickle.dump(symbols_set, file_writer)
                file_writer.write(b'\n')
                end_dict_pos = file_writer.tell()
                file_writer.write(b'0')

                self.init_minus_one_context(symbols_set)
                context = b""
                for i in range(data_len):
                    symbol = file_data[i:i+1]
                    encode_context = self.encode_symbol(context, symbol)

                    if self.update_exclusion:
                        self.update_model(context, encode_context, symbol)
                    else:
                        self.update_model(context, "", symbol)
                    # print(self.contexts)
                    context = (context + symbol)[-self.order:]

                bit_str = self.ac_compressor.end_encode()
                bit_cnt_added_to_last_byte = bits_buffer.write()

                file_writer.seek(end_dict_pos)
                file_writer.write(bit_cnt_added_to_last_byte.to_bytes(1, byteorder="big"))

        return bit_str