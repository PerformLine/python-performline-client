"""
Functions for converting data between various units.
"""
from __future__ import absolute_import


SI_UNITS = {
    0: ('', ''),
    1: ('Kilo', 'K'),
    2: ('Mega', 'M'),
    3: ('Giga', 'G'),
    4: ('Tera', 'T'),
    5: ('Peta', 'P'),
    6: ('Exa', 'E'),
    7: ('Zetta', 'Z'),
    8: ('Yotta', 'Y'),
    9: ('Bronto', 'B'),
}


def convert_to(value, to_unit, full_name=False, suffix='B', numeric_format='{0:d}'):
    exponent = 0
    suffix_lead = ''

    if to_unit is not None and len(to_unit) > 0:
        for exp, unit in SI_UNITS.items():
            if unit[1] == str(to_unit)[0].upper():
                exponent = exp
                if full_name:
                    suffix_lead = unit[0]
                else:
                    suffix_lead = unit[1]

                break

    if exponent:
        value = int(value) / (1024**exponent)

    return (numeric_format + '{1}{2}').format(
        value,
        suffix_lead,
        suffix
    )
