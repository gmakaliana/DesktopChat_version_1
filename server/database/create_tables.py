"""
Server Database Table Creation

Creates database tables required
by Desktop Chat Server.
"""


from database.db import get_connection





# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables():


    connection = get_connection()

    cursor = connection.cursor()



    # ======================================================
    # USERS
    # ======================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (

            user_id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            full_name TEXT NOT NULL,

            profile_picture TEXT,

            status TEXT DEFAULT 'Offline',

            last_seen TEXT,

            created_at TEXT NOT NULL

        )
        """
    )



    # ======================================================
    # CONTACTS
    # ======================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS contacts
        (

            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            friend_id INTEGER NOT NULL,


            UNIQUE(
                user_id,
                friend_id
            )

        )
        """
    )



    # ======================================================
    # CHAT MESSAGES
    # ======================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS chats
        (

            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,


            sender_id INTEGER NOT NULL,


            receiver_id INTEGER NOT NULL,


            message TEXT,


            message_type TEXT DEFAULT 'text',


            sent_at TEXT NOT NULL,


            is_read INTEGER DEFAULT 0


        )
        """
    )



    # ======================================================
    # FILES
    # ======================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS files
        (

            file_id INTEGER PRIMARY KEY AUTOINCREMENT,


            sender_id INTEGER NOT NULL,


            receiver_id INTEGER NOT NULL,


            file_name TEXT NOT NULL,


            file_path TEXT NOT NULL,


            file_type TEXT,


            file_size INTEGER,


            sent_at TEXT

        )
        """
    )



    connection.commit()


    connection.close()



    print(
        "Server database tables created."
    )





# ==========================================================
# TEST RUN
# ==========================================================

if __name__ == "__main__":

    create_tables()

    