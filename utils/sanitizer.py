def sanitize_column(col):
    replacements = {
        '|': '',
        ')': '',
        '(': '',
        '=': '',
        '«': '',
        ',': '',
        'i': '1',
        'A': '4',
        'o': '0',
        'O': '0',
        '§': '5'
    }

    for k, v in replacements.items():
        col = col.replace(k, v)

    return col
