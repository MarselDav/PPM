class BitsBuffer:
    def __init__(self):
        self.bytes = bytearray()
        self.current_bin_code = ""
        self.file_writer = None

    def set_file_writer(self, file_writer):
        self.file_writer = file_writer

    def add(self, code):
        self.current_bin_code += code
        if len(self.current_bin_code) >= 8:
            self.append()

    def append(self):
        self.bytes.append(int(self.current_bin_code[:8:], 2))
        self.current_bin_code = self.current_bin_code[8::]

    def write(self):
        bit_cnt_added_to_last_byte = 0
        if self.file_writer is not None:
            current_bin_code_cnt = len(self.current_bin_code)
            if current_bin_code_cnt > 0:
                self.current_bin_code = self.current_bin_code.ljust(8, "0")
                bit_cnt_added_to_last_byte = len(self.current_bin_code) - current_bin_code_cnt
                self.append()
            self.file_writer.write(self.bytes)
            self.bytes.clear()
        else:
            print("file_writer не существует")

        return bit_cnt_added_to_last_byte