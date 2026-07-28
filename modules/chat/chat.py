"""
Chat Management Module

Responsible for chat operations.

Responsibilities:
- Sending messages.
- Loading chat history.
- Formatting messages.
- Handling timestamps.
- Handling file downloads.

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
    save_chat_file
)




# ==========================================================
# GET CURRENT TIME
# ==========================================================

def get_current_time():

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )





# ==========================================================
# CHAT FILE STORAGE LOCATION
# ==========================================================

def get_chat_file_folder(file_type):


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
# DOWNLOAD CHAT FILE
# ==========================================================

def download_chat_file(
    relative_path,
    destination
):
    """
    Copies stored chat file
    to selected destination.


    Database stores:

        uploads/images/photo.jpg


    Function converts it into:

        C:/Users/User/Documents/Desktop Chat/uploads/images/photo.jpg

    """


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
            "Download file error:",
            error
        )


        return False





# ==========================================================
# SEND MESSAGE
# ==========================================================

def send_chat_message(
    sender_id,
    receiver_id,
    message
):


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
# SEND FILE
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




    # ======================================================
    # IMPORTANT CHANGE
    #
    # Convert absolute path:
    #
    # C:\Users\George\Documents\Desktop Chat\uploads\images\a.jpg
    #
    # INTO:
    #
    # uploads/images/a.jpg
    #
    # ======================================================


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
# MARK CONVERSATION READ
# ==========================================================

def mark_conversation_read(
    current_user_id,
    other_user_id
):


    return mark_messages_as_read(
        current_user_id,
        other_user_id
    )





# ==========================================================
# MARK SINGLE MESSAGE READ
# ==========================================================

def mark_as_read(
    chat_id
):


    return mark_message_read(
        chat_id
    )





# ==========================================================
# GET DISPLAY MESSAGES
# ==========================================================

def get_display_messages(
    current_user_id,
    other_user_id
):


    display_messages = []



    # ======================================================
    # TEXT MESSAGES
    # ======================================================


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

                "type": "message",

                "chat_id": message["chat_id"],

                "sender_id": message["sender_id"],

                "receiver_id": message["receiver_id"],

                "sender": sender,

                "message": message["message"],

                "time": timestamp,

                "is_read": message["is_read"],

                "sort_time": message["sent_at"]

            }

        )





    # ======================================================
    # FILE MESSAGES
    # ======================================================


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

                "type": "file",

                "file_id": file["file_id"],

                "sender_id": file["sender_id"],

                "receiver_id": file["receiver_id"],

                "sender": sender,

                "file_name": file["file_name"],


                # DATABASE NOW STORES RELATIVE PATH

                "stored_path": file["file_path"],


                "file_type": file["file_type"],

                "file_size": file["file_size"],

                "time": timestamp,

                "sort_time": file["sent_at"]

            }

        )





    # ======================================================
    # SORT ALL CHAT ITEMS
    # ======================================================


    display_messages.sort(
        key=lambda x: x["sort_time"]
    )



    return display_messages