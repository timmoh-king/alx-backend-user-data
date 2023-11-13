#!/usr/bin/env python3

"""
    Write a function `filter_datum` that returns the log message obfuscated:
"""

import os
import re
import csv
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """
         function takes no arguments and returns a logging.Logger object
         logger should be named "user_data" and only log up to logging.INFO
         It should have a StreamHandler with RedactingFormatter as formatter
         It should not propagate messages to other loggers.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
        Use the os module to obtain credentials from the environment
        Use the module mysql-connector-python to connect to the MySQL db
    """
    return mysql.connector.connect(
            host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
            port = 3306,
            user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
            password = os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
            database = os.getenv("PERSONAL_DATA_DB_NAME", "")
    )

def main() -> None:
    """
        The function will obtain a database connection using get_db
        retrieve all rows in the users table and display each row
        under a filtered format like this
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email, phone, ssn, password FROM users;")
    logger = get_logger()

    rows = cursor.fetchall()
    for row in rows:
        logger.info("name={};email={};phone={}ssn={};password={}".format(
            row[0], row[1], row[2], row[3], row[4]))

    cursor.close()
    db.close()
