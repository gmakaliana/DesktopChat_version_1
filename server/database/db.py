"""
Server Database Connection

Provides SQLite connection
for FastAPI WebSocket server.
"""


import sqlite3
from pathlib import Path



# ==========================================================
# DATABASE LOCATION
# ==========================================================


DATABASE_PATH = Path(
    "../chat.db"
)





# ==========================================================
# GET CONNECTION
# ==========================================================

def get_connection():
    """
    Creates SQLite connection.
    """


    connection = sqlite3.connect(
        DATABASE_PATH
    )


    connection.row_factory = sqlite3.Row


    return connection

