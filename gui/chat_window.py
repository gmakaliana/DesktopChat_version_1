"""
Chat Window

Displays conversation between two users.

Responsibilities:
- Display chat history.
- Send messages.
- Refresh messages.
- Handle message input.

Business logic:
    modules/chat/chat.py
"""


import tkinter as tk
from tkinter import ttk


from modules.chat.chat import (
    send_chat_message,
    get_display_messages
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



# ==========================================================
# LOAD MESSAGES
# ==========================================================

def load_messages(
    chat_box,
    current_user,
    selected_user
):
    """
    Loads chat history into display area.
    """


    chat_box.config(
        state="normal"
    )


    chat_box.delete(
        "1.0",
        tk.END
    )



    messages = get_display_messages(
        current_user["user_id"],
        selected_user["user_id"]
    )



    for message in messages:


        chat_box.insert(
            tk.END,
            message
        )



    chat_box.config(
        state="disabled"
    )


    # Auto scroll

    chat_box.see(
        tk.END
    )





# ==========================================================
# SEND MESSAGE
# ==========================================================

def send_message_action(
    message_entry,
    chat_box,
    current_user,
    selected_user
):
    """
    Sends a message.
    """


    message = message_entry.get().strip()



    if not message:

        return



    success = send_chat_message(
        current_user["user_id"],
        selected_user["user_id"],
        message
    )



    if success:


        # Clear input box

        message_entry.delete(
            0,
            tk.END
        )



        # Reload chat

        load_messages(
            chat_box,
            current_user,
            selected_user
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

    Args:
        parent:
            Home window.

        current_user:
            Logged in user.

        selected_user:
            Contact being chatted with.
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
        650,
        550
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
        text=(
            f"Chat with "
            f"{selected_user['full_name']}"
        ),
        font=TITLE_FONT,
        bg=BACKGROUND
    )


    title.pack(
        pady=(20,10)
    )



    # ======================================================
    # CHAT DISPLAY
    # ======================================================


    chat_box = tk.Text(
        window,
        wrap="word",
        state="disabled",
        font=NORMAL_FONT
    )


    chat_box.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )



    # ======================================================
    # MESSAGE INPUT AREA
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



    send_button = ttk.Button(
        input_frame,
        text="Send",
        command=lambda:

        send_message_action(
            message_entry,
            chat_box,
            current_user,
            selected_user
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
            selected_user
        )
    )



    # ======================================================
    # INITIAL LOAD
    # ======================================================


    load_messages(
        chat_box,
        current_user,
        selected_user
    )



    message_entry.focus()