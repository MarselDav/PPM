from PPM_compressor import PPM_compressor
from PPM_decompressor import PPM_decompressor
import time


if __name__ == "__main__":
     model_order = 4
     original_text = "files/test.txt"
     # original_text = "files/enwik7.txt"
     # original_text = "files/hamlet.txt"
     # original_text = "files/Evgeniy_Zamyatin_My.txt"
     # original_text = "files/war_and_peace.ru.txt"
     compressed_text = "files/compressed.txt"
     decompressed_text = "files/decompressed.txt"

     with open(original_text, "rb") as file_reader:
          length = len(file_reader.read())

     start_time = time.time_ns()
     cnt = 1
     for i in range(cnt):
          ppm_compressor = PPM_compressor(model_order, exclusion=True, update_exclusion=False)
          ppm_compressor.encode_data(original_text, compressed_text)

          ppm_decompressor = PPM_decompressor(model_order, exclusion=True, update_exclusion=False)
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

     # for model_order in range(1, 10):
     #      ppm_compressor = PPM_compressor(model_order,  exclusion=True, update_exclusion=True)
     #      ppm_compressor.encode_data(original_text, compressed_text)
     #
     #      ppm_decompressor = PPM_decompressor(model_order, exclusion=True,
     #                                          update_exclusion=True)
     #      ppm_decompressor.decode_data(length, compressed_text, decompressed_text)
     #
     #      with open(original_text, "rb") as file_reader:
     #           original_data = file_reader.read()
     #           orig_len = len(original_data)
     #
     #      with open(compressed_text, "rb") as file_reader:
     #           compressed_len = len(file_reader.read())
     #
     #      with open(decompressed_text, "rb") as file_reader:
     #           decompressed_data = file_reader.read()
     #
     #      print(original_data == decompressed_data)
     #      print(model_order, orig_len / compressed_len)

     # update_exclusion time 162_730_043_800
     # update_exclusion coeff 1.9105671174586094

     # without all time 193_415_312_800
     # without all coeff  1.8411252515667516

     # exclusion time 218643012700
     # exclusion coeff 1.946484901311269

     # with all exclusions time 173306956700
     # with all exclusions coeff 1.967441208921795
