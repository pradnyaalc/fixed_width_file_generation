import unittest

from fixed_width_gen import FixedWidth
from decimal import Decimal
import csv

class TestFixedWidthGen(unittest.TestCase):

    def test_get_config(self):
        config_file = "spec.json"
        fx = FixedWidth(config_file, data_file_name="fwf.txt")
        fx.close_file()

        conf = {'ColumnNames': ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10'], 'Offsets': ['5', '12', '3', '2', '13', '7', '10', '13', '20', '13'], 'FixedWidthEncoding': 'windows-1252', 'IncludeHeader': 'True', 'DelimitedEncoding': 'utf-8'}
        field_values = [('f1', 5), ('f2', 12), ('f3', 3), ('f4', 2), ('f5', 13), ('f6', 7), ('f7', 10), ('f8', 13), ('f9', 20), ('f10', 13)]

        self.assertEqual(fx.config, conf)
        self.assertEqual(fx.fields, field_values)

    def test_basic_line_generation(self):
        config_file = "spec.json"
        fx = FixedWidth(config_file, data_file_name="fwf.txt")
        fx.close_file()

        fx.update({"f1": "Ms", "f2": "Michael", "f3": 32, "f4": "vr", "f5": Decimal('40.7128'),
             "f6": Decimal('-74.005'), "f7": -100, "f8": Decimal('1.0001'), "f9": "abcdefg1234###q", "f10": "Pradnya"})
        line = fx.build_line()
        expected_line = "f1   f2          f3 f4f5           f6     f7        f8           f9                  f10          \n" + \
                        "Ms   Michael     32 vr40.7128      -74.005-100      1.0001       abcdefg1234###q     Pradnya      \n"
        self.assertEqual(line, expected_line)

    def test_fixed_width_empty_values(self):
        config_file = "spec.json"
        fx = FixedWidth(config_file, data_file_name="fwf.txt")
        fx.header = False
        fx.close_file()

        fx.update({"f1": "Ms", "f2": "Michael", "f3": 32, "f4": "", "f5": Decimal('40.7128'),
                   "f6": Decimal('-74.005'), "f7": -100, "f8": None, "f9": "abcdefg1234###q",
                   "f10": "Pradnya"})
        line = fx.build_line()
        expected_line = "Ms   Michael     32   40.7128      -74.005-100                   abcdefg1234###q     Pradnya      \n"
        self.assertEqual(line,expected_line)

    def test_parser(self):
        config_file = "spec.json"
        fx = FixedWidth(config_file, data_file_name="fwf.txt")
        # fx.header = False
        fx.close_file()

        fx.parser("fixed_width_file.txt", "test_csv.csv")

        reader = csv.DictReader(open("test_csv.csv", 'r', encoding='utf-8'))

        expected = [{"f1": "Ms", "f2": "Michael", "f3": '32', "f4": "vr", "f5": '40.7128',
             "f6": '-74.005', "f7": '-100', "f8": '1.0001', "f9": "abcdefg1234###q", "f10": "Pradnya"},
            {"f1": "Mr", "f2": "Smith", "f3": '32', "f4": "r", "f5": '38.7128',
             "f6": '-64.005', "f7": '-130', "f8": '1.0001', "f9": "abcdefg1234###q", "f10": "Alchetti"}]
        actual = []
        for row in reader:
            actual.append(dict(row))

        self.assertEqual(actual,expected)

if __name__ == '__main__':
    unittest.main()