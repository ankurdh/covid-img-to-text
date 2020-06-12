from ocr.OcrBase import OcrBase
from utils.rowparser import get_processed_data_row
from utils.sanitizer import sanitize_column


def get_jk_processed_data_row(row, totals_row = False):
    r = {}
    elements = row.split(' ')
    data_index = 1
    if not totals_row:
        data_index = 2
        # Skip the sl. no at col 1.
        # District name is second col
        if elements[1].isalpha():
            r['district'] = elements[1]
        else:
            r['district'] = elements[2]
            data_index = 3

    # we expect 10 numbers from data_index
    parsed_numbers = 0
    while True:
        if parsed_numbers == 10:
            break

        sanitize_column(elements[data_index])

        if elements[data_index] == '':
            data_index += 1
            continue

        if elements[data_index].isnumeric():
            r[JKOcrParser.header[1 + parsed_numbers]] = elements[data_index]
        else:
            r[JKOcrParser.header[1 + parsed_numbers]] = 'n/a'

        data_index += 1
        parsed_numbers += 1
    return r


class JKOcrParser(OcrBase):
    header = [
        'District',
        'Positive Today - Travelers',
        'Positive Today - Others',
        'Positive Today - Total',
        'Positive Cumulative - Travelers',
        'Positive Cumulative - Others',
        'Positive Cumulative - Total',
        'Active Positive',
        'Recovered Today',
        'Recovered Cumulative',
        'Deaths'
    ]

    def __init__(self, img):
        super().__init__(img)

    def process_ocr_text(self):
        ret = {}
        s = self.img_str.split('\n')
        s = [i for i in s if i]
        # Date is in the 1st line of JK bulletin
        ret['date'] = s[0].split(' ')[-1]

        # Data starts from 5th row
        data = []
        for i in range(4, 24):
            try:
                data.append(get_processed_data_row(s[i], 10, JKOcrParser))
            except:
                self.errors.append({
                    'Data': s[i],
                    'Extra info': 'Check for non alpha numeric chars, Check for 10 numbers to exist after district'
                })
        ret['data'] = data
        # Totals are in the 25th row
        ret['totals'] = get_processed_data_row(s[24], 10, JKOcrParser, totals_row=True)

        # Additional Info is the remainder of the text
        ret['additional_info'] = " ".join(s[25:])
        ret['errors'] = self.errors
        return self.img_str, ret
