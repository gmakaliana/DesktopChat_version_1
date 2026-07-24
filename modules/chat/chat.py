"""
Chat Management Module

Responsible for chat message operations.

Responsibilities:
- Send messages.
- Retrieve conversations.
- Mark messages as read.

Database operations are handled by:
    database/queries.py
"""


from datetime import datetime


from database.queries import (
    save_message,
    get_messages,
    mark_message_read
)



# ==========================================================
# SEND MESSAGE
# ==========================================================

def send_chat_message(
    sender_id,
    receiver_id,
    message
):
    """
    Sends a text message.

    Args:
        sender_id:
            User sending the message.

        receiver_id:
            User receiving the message.

        message:
            Text content.


    Returns:
        tuple:
            (True, message)
            (False, error)
    """



    # ======================================================
    # VALIDATION
    # ======================================================

    if message.strip() == "":

        return False, (
            "Message cannot be empty"
        )



    # Remove unnecessary spaces

    message = message.strip()



    # ======================================================
    # SAVE MESSAGE
    # ======================================================

    sent_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



    try:


        save_message(
            sender_id,
            receiver_id,
            message,
            sent_time
        )


        return True, (
            "Message sent"
        )



    except Exception:


        return False, (
            "Unable to send message"
        )



# ==========================================================
# GET CONVERSATION
# ==========================================================

def get_chat_history(
    user_one,
    user_two
):
    """
    Retrieves messages between two users.

    Args:
        user_one:
            First user ID.

        user_two:
            Second user ID.


    Returns:
        List of messages.
    """



    messages = get_messages(
        user_one,
        user_two
    )


    return messages



# ==========================================================
# MARK MESSAGE AS READ
# ==========================================================

def read_message(
    chat_id
):
    """
    Marks a message as read.

    Args:
        chat_id:
            Message identifier.
    """


    mark_message_read(
        chat_id
    )



# ==========================================================
# FORMAT MESSAGE DISPLAY
# ==========================================================

def format_message(
    message
):
    """
    Formats database message data
    for displaying in GUI.

    Args:
        message:
            SQLite row.


    Returns:
        Display string.
    """



    formatted = (
        f"{message['sent_at']}\n"
        f"{message['message']}"
    )


    return formatted