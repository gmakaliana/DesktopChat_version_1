"""
Server Database Queries

Handles database operations
used by the WebSocket server.
"""


from database.db import get_connection





# ==========================================================
# GET USER BY ID
# ==========================================================

def get_user_by_id(user_id):
    """
    Returns user by ID.
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
# SAVE MESSAGE
# ==========================================================

def save_message(
    sender_id,
    receiver_id,
    message,
    sent_at
):
    """
    Saves incoming chat message.

    Returns:

        True  success
        False failed
    """


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
                message_type,
                sent_at,
                is_read
            )

            VALUES
            (
                ?,
                ?,
                ?,
                'text',
                ?,
                0
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

        