from ocr.OcrBase import OcrBase
from utils.rowparser import get_processed_data_row
from utils.sanitizer import sanitize_column


def get_punjab_processed_data_row(row, totals_row = False):
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
        if parsed_numbers == 4:
            break

        sanitize_column(elements[data_index])

        if elements[data_index] == '':
            data_index += 1
            continue

        if elements[data_index].isnumeric():
            r[PunjabOcrParser.header[1 + parsed_numbers]] = elements[data_index]
        else:
            r[PunjabOcrParser.header[1 + parsed_numbers]] = 'n/a'

        data_index += 1
        parsed_numbers += 1
    return r


class PunjabOcrParser(OcrBase):
    header = [
        'District',
        'Total Confirmed',
        'Total Active',
        'Total Recovered',
        'Deaths'
    ]

    def __init__(self, img):
        super().__init__(img)

    def process_ocr_text(self):
        d = self.img_str.split('\n')
        d = [i for i in d if i]
        r = {
            'date': '', # Punjab Doesn't have a date field
        }

        # For pubjab, data is between rows 5-27
        data = []

        # UGLY to hardcode indices, but there's no other way right now than hoping
        for i in d[3:24]:
            try:
                data.append(get_processed_data_row(i, 4, PunjabOcrParser))
            except:
                self.errors.append({
                    'Data': i,
                    'Extra Info': 'Check for non alphanumeric chars and there should be 4 numbers after district'
                })
        r['data'] = data
        r['totals'] = get_processed_data_row(d[25], 4, PunjabOcrParser, totals_row=True)

        return self.img_str, r