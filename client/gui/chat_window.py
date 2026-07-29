"""
Chat Window

Displays conversation between two users.

Responsibilities:
- Display chat history.
- Send messages through WebSocket server.
- Receive real-time messages.
- Handle file attachments.
- Download received files.

Business logic:
    modules/chat/chat.py
"""


import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from pathlib import Path



from modules.chat.chat import (
    send_chat_file,
    get_display_messages,
    mark_conversation_read,
    download_chat_file
)



from modules.network.connection import (
    send_event,
    register_server_event,
    unregister_server_event
)



from utils.window_utils import (
    center_window,
    close_window
)



from utils.gui_theme import (
    BACKGROUND,
    TITLE_FONT,
    NORMAL_FONT
)



from utils.app_paths import (
    get_download_image_folder,
    get_download_document_folder,
    get_download_other_folder
)





# ==========================================================
# ACTIVE CHAT WINDOWS
# ==========================================================

# Stores opened chat windows
#
# {
#    (current_user_id, selected_user_id):
#           {
#              "window": window,
#              "chat_box": Text,
#              "refresh": function
#           }
# }

active_chat_boxes = {}







# ==========================================================
# RECEIVE MESSAGE EVENT
# ==========================================================

def handle_received_message(
    data
):
    """
    Handles incoming real-time message.

    Database remains the source of truth.
    We refresh the current chat only.
    """


    sender_id = data.get(
        "sender_id"
    )


    receiver_id = data.get(
        "receiver_id"
    )


    # Current receiver is the logged-in user,
    # sender is the other user.

    key = (
        receiver_id,
        sender_id
    )



    chat = active_chat_boxes.get(
        key
    )



    if not chat:

        return



    refresh = chat.get(
        "refresh"
    )



    if refresh:

        refresh()








# ==========================================================
# MESSAGE SENT EVENT
# ==========================================================

def handle_message_sent(
    data
):
    """
    Handles server delivery confirmation.
    """


    print(
        "Message delivered:",
        data
    )









# ==========================================================
# LOAD CHAT HISTORY
# ==========================================================

def load_messages(
    chat_box,
    current_user,
    selected_user,
    file_links
):


    chat_box.config(
        state="normal"
    )


    chat_box.delete(
        "1.0",
        tk.END
    )


    file_links.clear()



    mark_conversation_read(
        current_user["user_id"],
        selected_user["user_id"]
    )



    messages = get_display_messages(

        current_user["user_id"],

        selected_user["user_id"]

    )





    for message in messages:



        # ==================================================
        # FILE MESSAGE
        # ==================================================

        if message["type"] == "file":


            sender = (

                "You"

                if message["sender_id"]
                ==
                current_user["user_id"]

                else message["sender"]

            )



            chat_box.insert(

                tk.END,

                f"\n{sender}\n",

                "sender_name"

            )



            start = chat_box.index(
                tk.INSERT
            )



            chat_box.insert(

                tk.END,

                f"📎 {message['file_name']} (click to download)\n",

                "file_link"

            )



            end = chat_box.index(
                tk.INSERT
            )



            tag = (

                f"file_{message['file_id']}"

            )



            chat_box.tag_add(

                tag,

                start,

                end

            )



            file_links[tag] = {

                "path":
                message["stored_path"],

                "name":
                message["file_name"]

            }



            chat_box.tag_bind(

                tag,

                "<Button-1>",

                lambda event, t=tag:

                download_file_from_tag(

                    t,

                    file_links

                )

            )



            chat_box.insert(

                tk.END,

                message["time"] + "\n",

                "time"

            )



            continue







        # ==================================================
        # TEXT MESSAGE
        # ==================================================


        if message["sender_id"] == current_user["user_id"]:



            chat_box.insert(

                tk.END,

                "\nYou\n",

                "sender_name"

            )



            chat_box.insert(

                tk.END,

                message["message"] + "\n",

                "sender_message"

            )



            status = (

                "✓✓ Read"

                if message["is_read"]

                else "✓ Sent"

            )



            chat_box.insert(

                tk.END,

                f"{message['time']}   {status}\n",

                "time"

            )



        else:



            chat_box.insert(

                tk.END,

                f"\n{message['sender']}\n",

                "receiver_name"

            )



            chat_box.insert(

                tk.END,

                message["message"] + "\n",

                "receiver_message"

            )



            chat_box.insert(

                tk.END,

                message["time"] + "\n",

                "time"

            )






    chat_box.config(

        state="disabled"

    )


    chat_box.see(

        tk.END

    )








# ==========================================================
# SEND MESSAGE
# ==========================================================

def send_message_action(

    entry,

    current_user,

    selected_user

):


    message = entry.get().strip()



    if not message:

        return





    success = send_event(

        {

            "event":

            "message",


            "sender_id":

            current_user["user_id"],


            "receiver_id":

            selected_user["user_id"],


            "message":

            message

        }

    )





    if success:


        entry.delete(

            0,

            tk.END

        )







# ==========================================================
# SEND FILE
# ==========================================================

def attach_file_action(

    chat_box,

    current_user,

    selected_user,

    file_links

):


    file_path = filedialog.askopenfilename()



    if not file_path:

        return




    success = send_chat_file(

        current_user["user_id"],

        selected_user["user_id"],

        file_path

    )




    if success:


        load_messages(

            chat_box,

            current_user,

            selected_user,

            file_links

        )

# ==========================================================
# DOWNLOAD FILE
# ==========================================================

def download_file_from_tag(
    tag,
    file_links
):
    """
    Downloads attachment into
    the correct download folder.
    """


    file_info = file_links.get(
        tag
    )



    if not file_info:

        return



    file_name = file_info["name"]



    extension = Path(
        file_name
    ).suffix.lower()





    if extension in [

        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp"

    ]:


        folder = get_download_image_folder()



    elif extension in [

        ".pdf",
        ".doc",
        ".docx",
        ".xls",
        ".xlsx",
        ".txt"

    ]:


        folder = get_download_document_folder()



    else:


        folder = get_download_other_folder()





    destination = (

        folder

        /

        file_name

    )





    success = download_chat_file(

        file_info["path"],

        destination

    )





    if success:


        messagebox.showinfo(

            "Download Complete",

            f"{file_name}\n\nDownloaded successfully."

        )



    else:


        messagebox.showerror(

            "Download Failed",

            "Could not download file."

        )









# ==========================================================
# OPEN CHAT WINDOW
# ==========================================================

def open_chat_window(

    parent,

    current_user,

    selected_user

):


    window = tk.Toplevel(
        parent
    )



    window.title(

        f"Chat with {selected_user['full_name']}"

    )



    window.configure(

        background=BACKGROUND

    )



    window.resizable(

        True,

        True

    )



    center_window(

        window,

        700,

        600

    )



    window.transient(

        parent

    )



    window.grab_set()





    # ======================================================
    # HEADER
    # ======================================================


    title = tk.Label(

        window,

        text=f"Chat with {selected_user['full_name']}",

        font=TITLE_FONT,

        bg=BACKGROUND

    )


    title.pack(

        pady=(15,10)

    )







    # ======================================================
    # CHAT AREA
    # ======================================================


    chat_frame = ttk.Frame(

        window

    )


    chat_frame.pack(

        fill="both",

        expand=True,

        padx=15,

        pady=10

    )





    chat_box = tk.Text(

        chat_frame,

        wrap="word",

        state="disabled",

        font=NORMAL_FONT,

        padx=10,

        pady=10

    )



    chat_box.pack(

        side="left",

        fill="both",

        expand=True

    )





    scrollbar = ttk.Scrollbar(

        chat_frame,

        orient="vertical",

        command=chat_box.yview

    )



    scrollbar.pack(

        side="right",

        fill="y"

    )



    chat_box.configure(

        yscrollcommand=scrollbar.set

    )





    file_links = {}







    # ======================================================
    # CHAT IDENTIFIER
    # ======================================================


    key = (

        current_user["user_id"],

        selected_user["user_id"]

    )






    def refresh_chat():

        """
        Reload messages from database.
        """


        if window.winfo_exists():


            load_messages(

                chat_box,

                current_user,

                selected_user,

                file_links

            )







    active_chat_boxes[key] = {

        "window": window,

        "chat_box": chat_box,

        "refresh": refresh_chat

    }








    # ======================================================
    # TEXT FORMATTING
    # ======================================================


    chat_box.tag_configure(

        "sender_name",

        justify="right"

    )


    chat_box.tag_configure(

        "sender_message",

        justify="right"

    )


    chat_box.tag_configure(

        "receiver_name",

        justify="left"

    )


    chat_box.tag_configure(

        "receiver_message",

        justify="left"

    )


    chat_box.tag_configure(

        "time",

        justify="center"

    )



    chat_box.tag_configure(

        "file_link",

        foreground="blue",

        underline=True

    )








    # ======================================================
    # REGISTER EVENTS
    # ======================================================


    register_server_event(

        "message",

        handle_received_message

    )


    register_server_event(

        "message_sent",

        handle_message_sent

    )








    # ======================================================
    # INPUT AREA
    # ======================================================


    input_frame = ttk.Frame(

        window

    )


    input_frame.pack(

        fill="x",

        padx=15,

        pady=10

    )





    entry = ttk.Entry(

        input_frame

    )


    entry.pack(

        side="left",

        fill="x",

        expand=True

    )








    attach_button = ttk.Button(

        input_frame,

        text="📎 Attach",

        command=lambda:


        attach_file_action(

            chat_box,

            current_user,

            selected_user,

            file_links

        )

    )


    attach_button.pack(

        side="left",

        padx=5

    )







    send_button = ttk.Button(

        input_frame,

        text="Send",

        command=lambda:


        send_message_action(

            entry,

            current_user,

            selected_user

        )

    )


    send_button.pack(

        side="right"

    )







    entry.bind(

        "<Return>",

        lambda event:


        send_message_action(

            entry,

            current_user,

            selected_user

        )

    )







    # ======================================================
    # INITIAL LOAD
    # ======================================================


    load_messages(

        chat_box,

        current_user,

        selected_user,

        file_links

    )





    # ======================================================
    # BACKUP REFRESH
    # ======================================================


    def backup_refresh():


        if window.winfo_exists():


            refresh_chat()



            window.after(

                5000,

                backup_refresh

            )



    backup_refresh()



    entry.focus()







    # ======================================================
    # CLOSE WINDOW
    # ======================================================


    window.protocol(

        "WM_DELETE_WINDOW",

        lambda:


        close_chat_window(

            window,

            key

        )

    )









# ==========================================================
# CLOSE CHAT WINDOW
# ==========================================================

def close_chat_window(

    window,

    key

):


    unregister_server_event(

        "message",

        handle_received_message

    )


    unregister_server_event(

        "message_sent",

        handle_message_sent

    )




    if key in active_chat_boxes:


        del active_chat_boxes[key]


    close_window(

        window

    )