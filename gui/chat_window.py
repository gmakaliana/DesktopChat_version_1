"""
Chat Window

Displays conversation between two users.

Responsibilities:
- Display chat history.
- Send messages.
- Refresh messages.
- Handle message input.
- Display chat bubbles.

Business logic:
    modules/chat/chat.py
"""


import tkinter as tk
from tkinter import ttk, filedialog


from modules.chat.chat import (
    send_chat_message,
    send_chat_file,
    get_display_messages,
    mark_conversation_read,
    download_chat_file
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

from tkinter import messagebox
from pathlib import Path


from utils.app_paths import (
    get_download_image_folder,
    get_download_document_folder,
    get_download_other_folder
)

# ==========================================================
# LOAD MESSAGES
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

                if message["sender_id"] == current_user["user_id"]

                else message["sender"]

            )



            chat_box.insert(
                tk.END,
                "\n" + sender + "\n",
                "sender_name"
            )



            size_kb = round(
                message["file_size"] / 1024,
                2
            )



            start = chat_box.index(
                tk.INSERT
            )



            chat_box.insert(
                tk.END,
                f"📎 {message['file_name']} (Click to download)\n",
                "file_link"
            )



            end = chat_box.index(
                tk.INSERT
            )



            tag_name = (
                f"file_{message['file_id']}"
            )



            chat_box.tag_add(
                tag_name,
                start,
                end
            )



            # Store file information

            file_links[tag_name] = {

                "path": message["stored_path"],

                "name": message["file_name"]

            }



            # Make attachment clickable

            chat_box.tag_bind(
                tag_name,
                "<Button-1>",
                lambda event, tag=tag_name:

                download_file_from_tag(
                    tag,
                    file_links
                )
            )



            chat_box.insert(
                tk.END,
                f"{size_kb} KB\n",
                "time"
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
                "\n" + message["sender"] + "\n",
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
# AUTO REFRESH
# ==========================================================

def refresh_chat(
    window,
    chat_box,
    current_user,
    selected_user,
    file_links
):


    if not window.winfo_exists():

        return



    load_messages(
        chat_box,
        current_user,
        selected_user,
        file_links
    )



    window.after(
        2000,
        lambda:

        refresh_chat(
            window,
            chat_box,
            current_user,
            selected_user,
            file_links
        )
    )





# ==========================================================
# SEND MESSAGE
# ==========================================================

def send_message_action(
    message_entry,
    chat_box,
    current_user,
    selected_user,
    file_links
):


    message = message_entry.get().strip()



    if not message:

        return



    success = send_chat_message(
        current_user["user_id"],
        selected_user["user_id"],
        message
    )



    if success:


        message_entry.delete(
            0,
            tk.END
        )



        load_messages(
            chat_box,
            current_user,
            selected_user,
            file_links
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


    file_path = filedialog.askopenfilename(
        title="Select file"
    )



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
# DOWNLOAD FILE FROM LINK CLICK
# ==========================================================

def download_file_from_tag(
    tag_name,
    file_links
):
    """
    Automatically downloads attachment
    into correct download folder.
    """


    file_info = file_links.get(
        tag_name
    )


    if not file_info:

        return



    file_name = file_info["name"]


    extension = Path(
        file_name
    ).suffix.lower()



    # ======================================================
    # SELECT DOWNLOAD LOCATION
    # ======================================================

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
    """
    Opens chat window.
    """



    window = tk.Toplevel(
        parent
    )



    window.title(
        f"Chat with {selected_user['full_name']}"
    )



    window.resizable(
        True,
        True
    )



    window.configure(
        background=BACKGROUND
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





    window.protocol(
        "WM_DELETE_WINDOW",
        lambda:
        close_window(window)
    )





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
        pady=(20,10)
    )





    # ======================================================
    # CHAT DISPLAY
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





    # Stores file references

    file_links = {}





    # ======================================================
    # MESSAGE FORMATTING
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





    # ======================================================
    # FILE LINK STYLE
    # ======================================================

    chat_box.tag_configure(
        "file_link",
        foreground="blue",
        underline=True,
        font=("Arial", 10, "underline")
    )



    # Change cursor when mouse enters file

    chat_box.tag_bind(
        "file_link",
        "<Enter>",
        lambda event:

        chat_box.config(
            cursor="hand2"
        )
    )



    # Restore cursor when leaving file

    chat_box.tag_bind(
        "file_link",
        "<Leave>",
        lambda event:

        chat_box.config(
            cursor=""
        )
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





    message_entry = ttk.Entry(
        input_frame
    )



    message_entry.pack(
        side="left",
        fill="x",
        expand=True
    )





    # ======================================================
    # ATTACH FILE BUTTON
    # ======================================================

    attach_button = ttk.Button(
        input_frame,
        text="📎 Attach File",
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





    # ======================================================
    # SEND BUTTON
    # ======================================================

    send_button = ttk.Button(
        input_frame,
        text="Send",
        command=lambda:

        send_message_action(
            message_entry,
            chat_box,
            current_user,
            selected_user,
            file_links
        )
    )



    send_button.pack(
        side="right",
        padx=(10,0)
    )





    # ======================================================
    # ENTER KEY SEND
    # ======================================================

    message_entry.bind(
        "<Return>",
        lambda event:

        send_message_action(
            message_entry,
            chat_box,
            current_user,
            selected_user,
            file_links
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
    # START AUTO REFRESH
    # ======================================================

    window.after(
        2000,
        lambda:

        refresh_chat(
            window,
            chat_box,
            current_user,
            selected_user,
            file_links
        )
    )



    message_entry.focus()



