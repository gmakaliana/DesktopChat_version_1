"""
Database Connection Module
"""

import sqlite3

from utils.app_paths import get_database_path



def get_connection():
    """
    Creates SQLite connection.
    """

    database_path = get_database_path()


    connection = sqlite3.connect(
        database_path
    )


    connection.row_factory = sqlite3.Row


    return connection