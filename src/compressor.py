from utils.compressor.encode_data import encode_data
from utils.compressor.concat_symbols import concat_symbols
from utils.compressor.symbol_to_latin_encode import symbol_to_latin_encode


class Compressor():
    def __init__(self, data):
        self.data = data

    def run(self):
        current_dictionary_value, idx, encoded_message = 256, 0, []
        encode_dictionary = {(i.to_bytes(1, 'big')): i for i in range(256)}
        concatenated_ending, not_concatenated_ending = False, False

        while idx < len(self.data) - 1:
            symbol = encode_data(self.data, idx)
            next_symbol = encode_data(self.data, idx + 1)
            concatenated_symbols = concat_symbols(symbol, next_symbol)

            while concatenated_symbols in encode_dictionary:
                idx += 1
                symbol = concatenated_symbols
                if idx < len(self.data) - 1:
                    if concatenated_symbols not in encode_dictionary:
                        encode_dictionary[concatenated_symbols] = current_dictionary_value
                        encoded_message.append(
                            symbol_to_latin_encode(symbol, encode_dictionary))
                    concatenated_symbols = concat_symbols(
                        symbol, encode_data(self.data, idx + 1))
                else:
                    encoded_message.append(
                        symbol_to_latin_encode(symbol, encode_dictionary))
                    break

            if concatenated_symbols not in encode_dictionary:
                encode_dictionary[concatenated_symbols] = current_dictionary_value
                current_dictionary_value += 1
                encoded_message.append(
                    symbol_to_latin_encode(symbol, encode_dictionary))

                if idx == len(self.data) - 2:
                    encoded_message.append(
                        symbol_to_latin_encode(next_symbol, encode_dictionary))

            idx += 1

        return encoded_message