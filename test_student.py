import unittest
from proj3 import huffman_encoding

class TestHuffmanEncoding(unittest.TestCase):
    def test1(self):
        input_string = "test"
        expected_encoded = "100011"
        expected_codes = {'e': '00', 's': '01', 't': '1'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)

    def test2(self):
        input_string = "BEEP_BOOP"
        expected_encoded = "111000010110111010110"
        expected_codes = {'E': '00', 'O': '01', 'P': '10', '_': '110', 'B': '111'}
        encoded, decoded, codes = huffman_encoding(input_string)
        self.assertEqual(encoded, expected_encoded)
        self.assertEqual(decoded, input_string)
        self.assertEqual(codes, expected_codes)




if __name__ == "__main__":
    unittest.main()
