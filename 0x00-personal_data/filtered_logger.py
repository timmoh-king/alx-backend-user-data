#!/usr/bin/env python3
"""Module for filtering logs.

This module provides functions for filtering logs containing personally
identifiable information (PII). It includes a function to filter a single log
message, a function to create a logger for user data, a function to create a
connection to a database, and a main function to log information about user
records in a table.

Classes:
    RedactingFormatter: Formatter class for redacting PII fields from log
        messages.
"""
import os
import re
import logging
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """create a new instance"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a log"""
        filtered = filter_datum(self.fields, self.REDACTION,
                                record.getMessage(), self.SEPARATOR)
        record.msg = filtered
        return super().format(record)


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str
) -> str:
    """Filter a log message.

    Args:
        fields (List[str]): A list of PII fields to filter.
        redaction (str): The redaction string to use for the filtered fields.
        message (str): The log message to filter.
        separator (str): The separator character to use for the PII fields.

    Returns:
        str: The filtered log message.
    """
    extract, replace = (
        lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
        lambda x: r'\g<field>={}'.format(x))
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Create a logger for user data.

    Returns:
        logging.Logger: The logger object.
    """
    logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Create a connection to a database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection
        object.
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        port=3306,
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        database=os.getenv("PERSONAL_DATA_DB_NAME", ""),
    )


def main():
    """Entry Point Log information"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT name, email, phone, ssn, password, last_login,\
        user_agent FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info("name={};email={};phone={};ssn={};password={};\
                    last_login={};user_agent={};".
                    format(row[0], row[1], row[2], row[3], row[4],
                           row[5], row[6]))
    cursor.close()
    db.close()
