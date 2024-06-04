from PPM import PPM
from ArithmeticCodingDecompress import ArithmeticCodingDecompress
import pickle

class PPM_decompressor(PPM):
    def __init__(self, order, is_equally_probable=True, exclusion=False, update_exclusion=False):
        super().__init__(order, is_equally_probable, exclusion, update_exclusion)  # Вызов конструктора базового класса
        self.ac_compressor = None


    def decode_symbol(self, context):
        # len(context), а не self.order, потому что контекст может быть меньше, например для первого символа
        exclusion_symbols = set()
        for n in range(len(context), -1, -1):
            if context in self.contexts:

                if len(exclusion_symbols) > 0:
                    context_dict = {}

                    for key in self.contexts[context]:
                        if key not in exclusion_symbols or key == self.escape:
                            context_dict[key] = self.contexts[context][key]
                else:
                    context_dict = self.contexts[context]

                decode_symbol = self.ac_decompressor.decode_symbol(context_dict)
                if decode_symbol != self.escape:
                    return context, decode_symbol

                if self.exclusion:
                    exclusion_symbols.update(set(self.contexts[context].keys()))  # добавляем символы в исключения
            context = context[1::] # уменьшаем ебучий контекст

        decode_symbol = self.ac_decompressor.decode_symbol(self.contexts[-1])
        return -1, decode_symbol


    def decode_data(self, orig_data_len, file_input, file_output):
        with open(file_input, "rb") as file_reader:
            diffrent_symbols = pickle.load(file_reader)
            file_reader.readline()
            bit_cnt_added_to_last_byte = int.from_bytes(file_reader.read(1), byteorder="big")
            encoded_data = file_reader.read()

            self.ac_decompressor = ArithmeticCodingDecompress(orig_data_len)
            self.ac_decompressor.init_decoding(encoded_data, bit_cnt_added_to_last_byte)

            self.init_minus_one_context(diffrent_symbols)
            decode_data = bytearray()
            context = b""

            while len(decode_data) != orig_data_len:
                decode_context, decode_symbol = self.decode_symbol(context)
                decode_data += decode_symbol

                if self.update_exclusion:
                    self.update_model(context, decode_context, decode_symbol)
                else:
                    self.update_model(context, "", decode_symbol)

                context = (context + decode_symbol)[-self.order:]

        with open(file_output, "wb") as file_writer:
            file_writer.write(decode_data)