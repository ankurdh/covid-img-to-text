from utils.sanitizer import sanitize_column


def get_processed_data_row(row, total_expected_numeric_cols, header_cls, totals_row = False):
    r = {}
    elements = row.split(' ')
    if totals_row:
        data_index = 1
    else:
        if elements[1].isalpha():
            r['district'] = elements[1]
            data_index = 2
        else:
            r['district'] = elements[2]
            data_index = 3

    # We expect 4 numbers per row
    parsed_numbers = 0
    while True:
        if parsed_numbers == total_expected_numeric_cols:
            break

        sanitize_column(elements[data_index])

        if elements[data_index] == '':
            data_index += 1
            continue

        if elements[data_index].isnumeric():
            r[header_cls.header[1 + parsed_numbers]] = elements[data_index]
        else:
            r[header_cls.header[1 + parsed_numbers]] = 'n/a'

        data_index += 1
        parsed_numbers += 1
    return r
