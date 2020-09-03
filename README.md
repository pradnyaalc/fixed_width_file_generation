# Fixed width docker file generation

The application generates a fixed width file by reading the configuration for each column from spec.json.
It also parses the generated fixed width file to generate a csv file. The type of the data for each column is considered to be string.

## Spec.json
### Attributes
- **ColumnNames**: list of all the columns in string format
- **Offsets**: list of lengths for each column defined. Should be in string format
- **FixedWidthEncoding**: Type of encoding required to generate fixed width file
- **DelimitedEncoding**: Type of encoding required to generate csv file
- **IncludeHeader**: Boolean value (True adds the column names as header)

## Steps to run
1. Clone the repository
2. cd fixed_width_file_generation
3. docker build -t fixed-width-file .
4. docker run fixed-width-file
5. docker exec [container_name] bash
6. View the generated files
