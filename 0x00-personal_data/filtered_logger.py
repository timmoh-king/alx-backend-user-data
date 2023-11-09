#!/usr/bin/env python3

"""
    Write a function `filter_datum` that returns the log message obfuscated:
"""

import re
import logging
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
            Update the class to accept a list of strings fields const args
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
            filter values in incoming log records using filter_datum.
            Values for fields in fields should be filtered.
        """
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        record.msg = filtered
        return super().format(record)


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    """
        use a regex to replace occurrences of certain field values.
        use re.sub to perform the substitution with a single regex.
    """
    extract, replace = (
        lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        lambda x: r'\g<field>={}'.format(x))
    return re.sub(extract(fields, separator), replace(redaction), message)
