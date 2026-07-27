

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


# ==========================================================
# GET USER BY USERNAME
# ==========================================================

def get_user_by_username(username):
    """
    Retrieves a user using username.

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

    Returns:
        User row or None
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

        True  - successful
        False - failed
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



    except Exception as error:


        connection.rollback()


        print(
            "Create user error:",
            error
        )


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
    Updates user's online status.

    Returns:

        True  - successful
        False - failed
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



    except Exception as error:


        connection.rollback()


        print(
            "update_user_status error:",
            error
        )


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

        True  - successful
        False - failed
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



    except Exception as error:


        connection.rollback()


        print(
            "update_last_seen error:",
            error
        )


        return False



    finally:


        connection.close()


# ==========================================================
# CONTACT QUERIES
# ==========================================================


# ==========================================================
# SEARCH USERS FOR ADDING CONTACTS
# ==========================================================

def search_users(
    keyword,
    current_user_id
):
    """
    Searches users by:

    - Username
    - Full name

    Excludes:
    - Current logged-in user
    - Users already in contacts

    Returns:
        List of users
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            user_id,
            username,
            full_name,
            status,
            last_seen

        FROM users

        WHERE
        (
            username LIKE ?
            OR
            full_name LIKE ?
        )

        AND user_id != ?

        AND user_id NOT IN
        (
            SELECT friend_id
            FROM contacts
            WHERE user_id = ?
        )

        ORDER BY full_name ASC
        """,
        (
            f"%{keyword}%",
            f"%{keyword}%",
            current_user_id,
            current_user_id
        )
    )

    users = cursor.fetchall()

    connection.close()
 
    return users


# ==========================================================
# CHECK CONTACT EXISTS
# ==========================================================

def contact_exists(
    user_id,
    friend_id
):
    """
    Checks if contact relationship exists.

    Returns:

        True  - exists
        False - does not exist
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT 1

        FROM contacts

        WHERE

        user_id = ?

        AND

        friend_id = ?

        """,
        (
            user_id,
            friend_id
        )
    )


    result = cursor.fetchone()


    connection.close()



    return result is not None



# ==========================================================
# ADD TWO-WAY CONTACT
# ==========================================================

def add_contact(
    user_id,
    friend_id
):
    """
    Creates a two-way contact relationship.

    Example:

        User A adds User B


        Database:

        A -> B
        B -> A


    Returns:

        True  - successful
        False - failed
    """


    # Cannot add yourself

    if user_id == friend_id:

        return False



    # Prevent duplicates

    if contact_exists(
        user_id,
        friend_id
    ):


        return False



    connection = get_connection()

    cursor = connection.cursor()


    try:


        # --------------------------------------------------
        # First direction
        # User -> Friend
        # --------------------------------------------------

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



        # --------------------------------------------------
        # Reverse direction
        # Friend -> User
        # --------------------------------------------------

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
                friend_id,
                user_id
            )
        )



        connection.commit()


        return True



    except Exception as error:


        connection.rollback()


        print(
            "Add contact error:",
            error
        )


        return False



    finally:


        connection.close()



# ==========================================================
# REMOVE CONTACT
# ==========================================================

def remove_contact(
    user_id,
    friend_id
):
    """
    Removes both sides of friendship.

    Deletes:

        User A -> User B
        User B -> User A


    Returns:

        True  - successful
        False - failed
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:


        cursor.execute(
            """
            DELETE FROM contacts

            WHERE

            (
                user_id = ?

                AND

                friend_id = ?
            )

            OR

            (
                user_id = ?

                AND

                friend_id = ?
            )

            """,
            (
                user_id,
                friend_id,
                friend_id,
                user_id
            )
        )


        connection.commit()


        return True



    except Exception as error:


        connection.rollback()


        print(
            "Remove contact error:",
            error
        )


        return False



    finally:


        connection.close()



# ==========================================================
# GET CONTACTS WITH STATUS
# ==========================================================

def get_contacts(
    user_id
):
    """
    Returns all user's contacts.

    Includes:

    - User ID
    - Username
    - Full name
    - Online/offline status
    - Last seen


    Returns:

        List of sqlite rows
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT


            users.user_id,

            users.username,

            users.full_name,

            users.status,

            users.last_seen



        FROM contacts



        JOIN users


        ON contacts.friend_id = users.user_id



        WHERE contacts.user_id = ?



        ORDER BY users.full_name ASC


        """,
        (
            user_id,
        )
    )



    contacts = cursor.fetchall()


    connection.close()


    return contacts


# ==========================================================
# GET CONTACT
# ==========================================================

def get_contact(
    user_id,
    friend_id
):
    """
    Returns a single contact.

    Returns:
        sqlite3.Row or None
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            users.user_id,
            users.username,
            users.full_name,
            users.status,
            users.last_seen

        FROM contacts

        JOIN users
        ON contacts.friend_id = users.user_id

        WHERE contacts.user_id = ?
        AND contacts.friend_id = ?
        """,
        (
            user_id,
            friend_id
        )
    )

    contact = cursor.fetchone()

    connection.close()

    return contact

# ==========================================================
# COUNT CONTACTS
# ==========================================================

def get_contact_count(user_id):
    """
    Returns number of contacts.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM contacts

        WHERE user_id = ?
        """,
        (
            user_id,
        )
    )

    count = cursor.fetchone()[0]

    connection.close()

    return count


# ==========================================================
# CHAT QUERIES
# ==========================================================


# ==========================================================
# SAVE MESSAGE
# ==========================================================

def save_message(
    sender_id,
    receiver_id,
    message,
    sent_at
):
    """
    Saves a chat message.

    Returns:

        True  - successful
        False - failed
    """

    # Remove leading/trailing whitespace
    message = message.strip()

    # Do not save empty messages
    if not message:
        return False

    connection = get_connection()

    cursor = connection.cursor()

    try:

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

        return True

    except Exception as error:

        connection.rollback()

        print(
            "Save message error:",
            error
        )

        return False

    finally:

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

    Includes:

    - Message ID
    - Sender ID
    - Receiver ID
    - Message text
    - Timestamp
    - Sender name


    Returns:

        List of messages
    """


    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(
        """
        SELECT


            chats.chat_id,


            chats.sender_id,


            chats.receiver_id,


            chats.message,


            chats.sent_at,


            chats.is_read,


            users.full_name AS sender_name



        FROM chats



        JOIN users



        ON chats.sender_id = users.user_id



        WHERE


        (
            chats.sender_id = ?

            AND

            chats.receiver_id = ?
        )



        OR



        (
            chats.sender_id = ?

            AND

            chats.receiver_id = ?
        )



        ORDER BY chats.sent_at ASC


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

    Returns:

        True  - successful
        False - failed
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:


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


        return True



    except Exception as error:


        connection.rollback()


        print(
            "Mark message read error:",
            error
        )


        return False



    finally:


        connection.close()

# ==========================================================
# MARK ALL RECEIVED MESSAGES AS READ
# ==========================================================

def mark_messages_as_read(
    receiver_id,
    sender_id
):
    """
    Marks all messages from another user as read.

    Used when opening conversation.
    """


    connection = get_connection()

    cursor = connection.cursor()


    try:

        cursor.execute(
            """
            UPDATE chats

            SET is_read = 1

            WHERE receiver_id = ?

            AND sender_id = ?

            """,
            (
                receiver_id,
                sender_id
            )
        )


        connection.commit()


        return True



    except Exception as error:


        connection.rollback()


        print(
            "Mark messages read error:",
            error
        )


        return False



    finally:

        connection.close()


