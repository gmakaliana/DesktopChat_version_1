"""
Database Query Module

Responsible for all database operations.

This module communicates directly with SQLite
through database/db.py.

Other parts of the application should NOT
write SQL queries directly.

Responsibilities:
- User queries
- Contact queries
- Chat queries
"""


from database.db import get_connection



# ==========================================================
# USER QUERIES
# ==========================================================


def get_user_by_username(username):
    """
    Retrieves a user using username.

    Args:
        username:
            Username to search.

    Returns:
        User row or None
    """


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (
            username,
        )
    )


    user = cursor.fetchone()


    connection.close()


    return user



# ==========================================================
# GET USER BY ID
# ==========================================================

def get_user_by_id(user_id):
    """
    Retrieves user using user ID.
    """


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE user_id = ?
        """,
        (
            user_id,
        )
    )


    user = cursor.fetchone()


    connection.close()


    return user



# ==========================================================
# CREATE USER
# ==========================================================

def create_user(
    username,
    password,
    full_name,
    created_at
):
    """
    Creates a new user account.

    Returns:
        True if successful
        False if failed
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:


        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password,
                full_name,
                created_at
            )

            VALUES
            (
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                username,
                password,
                full_name,
                created_at
            )
        )


        connection.commit()


        return True



    except Exception:


        connection.rollback()


        return False



    finally:


        connection.close()



# ==========================================================
# UPDATE USER STATUS
# ==========================================================

def update_user_status(
    user_id,
    status
):
    """
    Updates online/offline status.

    Returns:
        True  - if update was successful
        False - if an error occurred
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            UPDATE users
            SET status = ?
            WHERE user_id = ?
            """,
            (
                status,
                user_id
            )
        )


        connection.commit()


        return True



    except Exception:


        connection.rollback()


        return False



    finally:


        connection.close()


# ==========================================================
# UPDATE LAST SEEN
# ==========================================================

def update_last_seen(
    user_id,
    last_seen
):
    """
    Updates user's last seen time.

    Returns:
        True  - if update was successful
        False - if an error occurred
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            UPDATE users
            SET last_seen = ?
            WHERE user_id = ?
            """,
            (
                last_seen,
                user_id
            )
        )


        connection.commit()


        return True



    except Exception:


        connection.rollback()


        return False



    finally:


        connection.close()


# ==========================================================
# SEARCH USERS
# ==========================================================

def search_users(keyword):
    """
    Searches users by username or full name.

    Used when adding contacts.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT *
        FROM users

        WHERE username LIKE ?
        OR full_name LIKE ?
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%"
        )
    )



    users = cursor.fetchall()


    connection.close()


    return users



# ==========================================================
# CONTACT QUERIES
# ==========================================================


def add_contact(
    user_id,
    friend_id
):
    """
    Adds a new contact relationship.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        INSERT INTO contacts
        (
            user_id,
            friend_id
        )

        VALUES
        (
            ?,
            ?
        )
        """,
        (
            user_id,
            friend_id
        )
    )



    connection.commit()


    connection.close()



# ==========================================================
# GET CONTACTS
# ==========================================================

def get_contacts(user_id):
    """
    Returns all contacts belonging to a user.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT users.*

        FROM contacts

        JOIN users
        ON contacts.friend_id = users.user_id

        WHERE contacts.user_id = ?
        """,
        (
            user_id,
        )
    )



    contacts = cursor.fetchall()


    connection.close()


    return contacts



# ==========================================================
# CHAT QUERIES
# ==========================================================


def save_message(
    sender_id,
    receiver_id,
    message,
    sent_at
):
    """
    Saves a text message.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        INSERT INTO chats
        (
            sender_id,
            receiver_id,
            message,
            sent_at
        )

        VALUES
        (
            ?,
            ?,
            ?,
            ?
        )
        """,
        (
            sender_id,
            receiver_id,
            message,
            sent_at
        )
    )



    connection.commit()


    connection.close()



# ==========================================================
# GET CHAT HISTORY
# ==========================================================

def get_messages(
    user_one,
    user_two
):
    """
    Retrieves conversation between two users.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT *

        FROM chats

        WHERE
        (sender_id = ? AND receiver_id = ?)

        OR

        (sender_id = ? AND receiver_id = ?)

        ORDER BY sent_at ASC
        """,
        (
            user_one,
            user_two,
            user_two,
            user_one
        )
    )



    messages = cursor.fetchall()


    connection.close()


    return messages



# ==========================================================
# MARK MESSAGE AS READ
# ==========================================================

def mark_message_read(
    chat_id
):
    """
    Marks a message as read.
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        UPDATE chats

        SET is_read = 1

        WHERE chat_id = ?
        """,
        (
            chat_id,
        )
    )



    connection.commit()


    connection.close()