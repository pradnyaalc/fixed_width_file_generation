#!/usr/bin/python

# importing libraries
import json
from copy import deepcopy
from decimal import Decimal
import time


class FixedWidth:

    def get_config(self, config_file):
        """
        reads the json specification file and returns a dictionary
        :param config_file: json
        :return: dict
        """
        with open(config_file) as json_file:
            data = json.load(json_file)
            return data

    def __init__(self, config_file, **kwargs):
        self.config = self.get_config(config_file)
        self.fixed_width_encoding = self.config['FixedWidthEncoding']
        self.header = self.config['IncludeHeader']
        self.delimited_encoding = self.config['DelimitedEncoding']

        self.data = {}

        # '\n' to append at the end of each fixed with line
        self.line_end = kwargs.pop('line_end', '\n')
        self.file = open(kwargs['data_file_name'], 'w', encoding=self.fixed_width_encoding)

        # check for required attributes in the json specification
        if any([x not in self.config.keys() for x in
                ('ColumnNames', 'Offsets', 'FixedWidthEncoding', 'IncludeHeader', 'DelimitedEncoding')]):
            raise ValueError(
                "Not all required attributes are provided for generating the fixed width file")

        #check if the number of columns and the number of offsets are equal
        if len(self.config['ColumnNames']) != len(self.config['Offsets']):
            raise ValueError(
                "Number of fields and the number of offsets should be equal"
            )

        for key, value in self.config.items():
            # check the type of the attribute values in the config file
            if isinstance(value, list):
                if not all(isinstance(x, str) for x in value):
                    raise ValueError(
                        "The elements in %s have invalid type. Allowed: 'string'" % (key))
            elif not isinstance(value, str):
                raise ValueError(
                    "Invalid value type for %s. Allowed: 'string'" % (key))

        # generate a list of columns along with their lengths/offsets
        field_list = []
        for i in range(len(self.config['ColumnNames'])):
            field_list.append((self.config['ColumnNames'][i], int(self.config['Offsets'][i])))

        self.fields = deepcopy(field_list)

    def update(self, data_values):
        self.data.update(data_values)

    def validate_data(self):
        """
        checks whether the given data is valid or invalid
        :return: Boolean
        """
        for field in self.fields:
            field_name = field[0]
            length = field[1]

            # check if the required field names are present in the data
            if field_name in self.data:

                data = self.data[field_name]

                # ensure value passed in is not too long for the field
                field_data = self.format_field(field_name)
                if len(str(field_data)) > length:
                    raise ValueError("%s is too long (limited to %d \
                        characters)." % (field_name, length))

            else:  # no value passed in

                # if required but not provided
                if field_name in self.config["ColumnNames"]:
                    raise ValueError("Field %s is required, but was \
                        not provided." % (field_name,))

        return True

    def format_field(self, field):
        """
        format the data for each field and convert them into string
        :param field: input the field_name
        :return: string format of the data corresponding to field name
        """
        data = self.data[field]
        if data is None:
            return ''
        return str(data)

    def build_line(self):
        """
        Build fixed width line depending upon the lengths mentioned in config
        :return: line: fixed width line
        """
        self.validate_data()
        line = ''

        # add header if true
        if self.header:
            for x in self.fields:
                dat = x[0]
                justify = dat.ljust

                dat = justify(x[1], " ")

                line += dat

            line += self.line_end
            self.header = False

        for x in self.fields:
            field = x[0]
            length = x[1]
            if field in self.data:
                dat = self.format_field(field)
            else:
                dat = ''

            # left justify the string
            justify = dat.ljust

            dat = justify(length, " ")

            line += dat

        return line + self.line_end

    def write_file(self):
        """
        write the fixed width line into the file with specified encoding
        :return:
        """
        line = self.build_line()
        self.file.write(line)

    def close_file(self):
        self.file.close()

    def parser(self, data_file, csv_file):
        """
        Parse the given fixed width file and convert it into csv file with given encoding
        :param data_file: fixed with file
        :param csv_file: csv file name to generate
        :return:
        """
        try:
            read_file = open(data_file, 'r', encoding=self.fixed_width_encoding)
        except IOError:
            raise IOError("Could not read the file %s" % (data_file))

        try:
            write_file = open(csv_file, 'w', encoding=self.delimited_encoding)
        except IOError:
            raise IOError("Could not write to the file %s" % (csv_file))

        for line in read_file:
            parts = []
            counter = 0
            for field in self.fields:
                parts.append(line[counter:counter + field[1]].strip())
                counter += field[1]

            write_file.write(",".join(parts) + "\n")

        read_file.close()
        write_file.close()


def main():
    data = [{"f1": "Ms", "f2": "Michael", "f3": 32, "f4": "vr", "f5": Decimal('40.7128'),
             "f6": Decimal('-74.005'), "f7": -100, "f8": Decimal('1.0001'), "f9": "abcdefg1234###q", "f10": "Pradnya"},
            {"f1": "Mr", "f2": "Smith", "f3": 32, "f4": "r", "f5": Decimal('38.7128'),
             "f6": Decimal('-64.005'), "f7": -130, "f8": Decimal('1.0001'), "f9": "abcdefg1234###q", "f10": "Alchetti"}]

    config_file = "spec.json"
    fx = FixedWidth(config_file, data_file_name='fixed_width_file.txt')
    for each in data:
        fx.update(each)
        fx.write_file()

    fx.close_file()
    fx.parser("fixed_width_file.txt", "fixed_width_file_csv.csv")

    while True:
        print("Done converting and parsing")

    #time.sleep(300)


if __name__ == '__main__':
    main()
