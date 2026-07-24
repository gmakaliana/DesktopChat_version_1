"""
Database Table Creation Module

Responsible for creating all database tables
required by the Desktop Chat System.

This module should be executed once when the
application starts. If the tables already exist,
they will not be recreated.
"""

from database.db import get_connection


# ==========================================================
# CREATE DATABASE TABLES
# ==========================================================

def create_tables():
    """
    Creates all required database tables.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # ======================================================
    # USERS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            profile_picture TEXT,
            status TEXT DEFAULT 'Offline',
            last_seen TEXT,
            created_at TEXT NOT NULL
        )
    """)

    # ======================================================
    # CONTACTS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (

            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            friend_id INTEGER NOT NULL,


            UNIQUE(
                user_id,
                friend_id
            ),


            FOREIGN KEY(user_id)
                REFERENCES users(user_id),


            FOREIGN KEY(friend_id)
                REFERENCES users(user_id)

        )
    """)

    # ======================================================
    # CHATS TABLE
    # ======================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            message TEXT,
            message_type TEXT DEFAULT 'text',
            file_name TEXT,
            sent_at TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,

            FOREIGN KEY (sender_id)
                REFERENCES users(user_id),

            FOREIGN KEY (receiver_id)
                REFERENCES users(user_id)
        )
    """)

    # ======================================================
    # SAVE CHANGES
    # ======================================================

    connection.commit()

    # ======================================================
    # CLOSE DATABASE
    # ======================================================

    connection.close()