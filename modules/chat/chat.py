"""
Chat Management Module

Responsible for chat operations.

Responsibilities:
- Sending messages.
- Loading chat history.
- Formatting messages.
- Handling timestamps.

GUI should not communicate directly
with database queries.
"""


from datetime import datetime

from database.queries import (
    save_message,
    get_messages,
    mark_message_read,
    mark_messages_as_read
)


# ==========================================================
# GET CURRENT TIME
# ==========================================================

def get_current_time():
    """
    Returns current date and time.

    Format:
    YYYY-MM-DD HH:MM:SS
    """


    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
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
    Sends and saves a chat message.

    Args:
        sender_id:
            User sending message.

        receiver_id:
            User receiving message.

        message:
            Text content.


    Returns:
        True/False
    """


    message = message.strip()



    if not message:

        return False



    sent_at = get_current_time()



    success = save_message(
        sender_id,
        receiver_id,
        message,
        sent_at
    )



    return success





# ==========================================================
# LOAD CHAT HISTORY
# ==========================================================

def load_chat_history(
    user_one,
    user_two
):
    """
    Loads previous conversation.

    Returns:
        List of messages
    """


    messages = get_messages(
        user_one,
        user_two
    )



    return messages





# ==========================================================
# FORMAT MESSAGE FOR DISPLAY
# ==========================================================

def format_message(
    message,
    current_user_id
):
    """
    Converts database message row
    into display text.


    Example:

    George [10:30]
    Hello


    """


    sender = message["sender_name"]


    timestamp = message["sent_at"]



    # Only show time part

    try:

        time = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S"
        ).strftime(
            "%H:%M"
        )


    except Exception:


        time = timestamp



    if message["sender_id"] == current_user_id:


        prefix = "You"


    else:


        prefix = sender



    formatted = (

        f"{prefix} [{time}]\n"

        f"{message['message']}\n\n"

    )



    return formatted





# ==========================================================
# MARK MESSAGE READ
# ==========================================================

def mark_as_read(
    chat_id
):
    """
    Marks a message as read.
    """


    return mark_message_read(
        chat_id
    )

# ==========================================================
# MARK CONVERSATION AS READ
# ==========================================================

def mark_conversation_read(
    current_user_id,
    other_user_id
):
    """
    Marks incoming messages as read.
    """


    return mark_messages_as_read(
        current_user_id,
        other_user_id
    )

# ==========================================================
# LOAD CHAT MESSAGES FOR GUI
# ==========================================================

def get_display_messages(
    current_user_id,
    other_user_id
):
    """
    Loads chat history and prepares
    messages for chat bubble display.

    Returns:

    [
        {
            sender_id,
            sender,
            message,
            time
        }
    ]

    """


    messages = load_chat_history(
        current_user_id,
        other_user_id
    )


    display_messages = []



    for message in messages:


        timestamp = message["sent_at"]



        try:

            time = datetime.strptime(
                timestamp,
                "%Y-%m-%d %H:%M:%S"
            ).strftime(
                "%H:%M"
            )


        except Exception:


            time = timestamp



        if message["sender_id"] == current_user_id:

            sender = "You"


        else:

            sender = message["sender_name"]



        display_messages.append(

            {
                "chat_id": message["chat_id"],

                "sender_id": message["sender_id"],

                "receiver_id": message["receiver_id"],

                "sender": sender,

                "message": message["message"],

                "time": time,

                "is_read": message["is_read"]

            }

        )



    return display_messages
