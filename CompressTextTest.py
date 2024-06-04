from PPM_compressor import PPM_compressor
from PPM_decompressor import PPM_decompressor
import time


if __name__ == "__main__":
     model_order = 4
     original_text = "test.txt"
     # original_text = "enwik7.txt"
     # original_text = "war_and_peace.ru.txt"
     compressed_text = "compressed.txt"
     decompressed_text = "decompressed.txt"

     with open(original_text, "rb") as file_reader:
          length = len(file_reader.read())

     start_time = time.time_ns()
     cnt = 1
     for i in range(cnt):
          ppm_compressor = PPM_compressor(model_order)
          ppm_compressor.encode_data(original_text, compressed_text)

          ppm_decompressor = PPM_decompressor(model_order)
          ppm_decompressor.decode_data(length, compressed_text, decompressed_text)
     end_time = time.time_ns()
     print((end_time - start_time) // cnt)


     with open(original_text, "rb") as file_reader:
          original_data = file_reader.read()
          orig_len = len(original_data)

     with open(compressed_text, "rb") as file_reader:
          compressed_len = len(file_reader.read())

     with open(decompressed_text, "rb") as file_reader:
          decompressed_data = file_reader.read()

     print(original_data == decompressed_data)
     print(orig_len / compressed_len)