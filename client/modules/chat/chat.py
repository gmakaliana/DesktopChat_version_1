"""
Chat Management Module

Responsible for chat data operations.

Responsibilities:
- Save messages locally.
- Load chat history.
- Format messages.
- Handle timestamps.
- Handle file storage.
- Handle file downloads.
- Manage unread messages.

Live message delivery is handled by:
    WebSocket Client

GUI should not communicate directly
with database queries.
"""


from datetime import datetime
from pathlib import Path
import os
import shutil



from utils.app_paths import (
    get_image_folder,
    get_upload_folder,
    get_document_folder,
    get_other_folder,
    get_relative_file_path,
    get_absolute_file_path
)



from database.queries import (
    save_message,
    get_messages,
    get_chat_files,
    mark_message_read,
    mark_messages_as_read,
    save_chat_file,
    get_unread_message_count,
    get_total_unread_messages
)





# ==========================================================
# CURRENT TIME
# ==========================================================

def get_current_time():

    return datetime.now().strftime(

        "%Y-%m-%d %H:%M:%S"

    )







# ==========================================================
# UNREAD COUNT
# ==========================================================

def get_contact_unread_count(
    current_user_id,
    contact_id
):

    return get_unread_message_count(

        current_user_id,

        contact_id

    )





def get_unread_count(
    user_id
):

    return get_total_unread_messages(

        user_id

    )







# ==========================================================
# FILE STORAGE LOCATION
# ==========================================================

def get_chat_file_folder(
    file_type
):


    extension = file_type.lower()



    if extension in [

        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp"

    ]:


        return get_image_folder()



    elif extension in [

        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".txt"

    ]:


        return get_document_folder()



    else:


        return get_other_folder()







# ==========================================================
# SAVE MESSAGE
# ==========================================================

def save_chat_message(
    sender_id,
    receiver_id,
    message
):
    """
    Saves message into local database.

    WebSocket handles delivery.
    Database stores history.
    """


    message = message.strip()



    if not message:

        return False



    return save_message(

        sender_id,

        receiver_id,

        message,

        get_current_time()

    )






# ==========================================================
# SEND MESSAGE COMPATIBILITY
# ==========================================================

def send_chat_message(
    sender_id,
    receiver_id,
    message
):
    """
    Compatibility wrapper.

    Old GUI code can still call this.

    New system should use:

        WebSocket send_event()

    """

    return save_chat_message(

        sender_id,

        receiver_id,

        message

    )







# ==========================================================
# SAVE FILE MESSAGE
# ==========================================================

def send_chat_file(
    sender_id,
    receiver_id,
    original_file_path
):


    if not os.path.exists(

        original_file_path

    ):

        return False





    file_name = os.path.basename(

        original_file_path

    )



    file_type = os.path.splitext(

        file_name

    )[1]



    file_size = os.path.getsize(

        original_file_path

    )





    folder = get_chat_file_folder(

        file_type

    )



    destination = (

        folder

        /

        file_name

    )




    try:


        shutil.copy2(

            original_file_path,

            destination

        )


    except Exception as error:


        print(

            "File copy error:",

            error

        )


        return False






    relative_path = get_relative_file_path(

        destination

    )





    return save_chat_file(

        sender_id,

        receiver_id,

        file_name,

        relative_path,

        file_type,

        file_size,

        get_current_time()

    )








# ==========================================================
# DOWNLOAD FILE
# ==========================================================

def download_chat_file(
    relative_path,
    destination
):


    try:


        actual_file_path = get_absolute_file_path(

            relative_path

        )



        shutil.copy2(

            actual_file_path,

            destination

        )



        return True



    except Exception as error:


        print(

            "Download error:",

            error

        )


        return False







# ==========================================================
# LOAD CHAT HISTORY
# ==========================================================

def load_chat_history(
    user_one,
    user_two
):


    return get_messages(

        user_one,

        user_two

    )








# ==========================================================
# MARK READ
# ==========================================================

def mark_conversation_read(
    current_user_id,
    other_user_id
):


    return mark_messages_as_read(

        current_user_id,

        other_user_id

    )






def mark_as_read(
    chat_id
):


    return mark_message_read(

        chat_id

    )








# ==========================================================
# FORMAT CHAT DISPLAY
# ==========================================================

def get_display_messages(
    current_user_id,
    other_user_id
):


    display_messages = []




    messages = load_chat_history(

        current_user_id,

        other_user_id

    )





    for message in messages:


        timestamp = datetime.strptime(

            message["sent_at"],

            "%Y-%m-%d %H:%M:%S"

        ).strftime(

            "%H:%M"

        )



        sender = (

            "You"

            if message["sender_id"] == current_user_id

            else message["sender_name"]

        )



        display_messages.append(

            {

                "type":

                "message",


                "chat_id":

                message["chat_id"],


                "sender_id":

                message["sender_id"],


                "receiver_id":

                message["receiver_id"],


                "sender":

                sender,


                "message":

                message["message"],


                "time":

                timestamp,


                "is_read":

                message["is_read"],


                "sort_time":

                message["sent_at"]

            }

        )







    files = get_chat_files(

        current_user_id,

        other_user_id

    )





    for file in files:


        timestamp = datetime.strptime(

            file["sent_at"],

            "%Y-%m-%d %H:%M:%S"

        ).strftime(

            "%H:%M"

        )



        sender = (

            "You"

            if file["sender_id"] == current_user_id

            else file["sender_name"]

        )



        display_messages.append(

            {

                "type":

                "file",


                "file_id":

                file["file_id"],


                "sender_id":

                file["sender_id"],


                "receiver_id":

                file["receiver_id"],


                "sender":

                sender,


                "file_name":

                file["file_name"],


                "stored_path":

                file["file_path"],


                "file_type":

                file["file_type"],


                "file_size":

                file["file_size"],


                "time":

                timestamp,


                "sort_time":

                file["sent_at"]

            }

        )





    display_messages.sort(

        key=lambda x: x["sort_time"]

    )



    return display_messages

