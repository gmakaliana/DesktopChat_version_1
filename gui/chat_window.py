"""
Chat Window

Provides the graphical interface for
one-to-one messaging.

Responsibilities:
- Display chat history.
- Send text messages.
- Refresh conversation.

Business logic is handled by:
    modules/chat/chat.py
"""


import tkinter as tk
from tkinter import ttk, messagebox


from modules.chat.chat import (
    send_chat_message,
    get_chat_history
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
    messages_box,
    current_user,
    selected_user
):
    """
    Loads conversation history
    between two users.
    """



    messages_box.config(
        state="normal"
    )


    messages_box.delete(
        "1.0",
        tk.END
    )



    messages = get_chat_history(
        current_user["user_id"],
        selected_user["user_id"]
    )



    for message in messages:


        if message["sender_id"] == current_user["user_id"]:

            sender = "You"

        else:

            sender = selected_user["full_name"]



        messages_box.insert(
            tk.END,
            (
                f"{sender}\n"
                f"{message['message']}\n"
                f"{message['sent_at']}\n\n"
            )
        )



    messages_box.config(
        state="disabled"
    )



# ==========================================================
# SEND MESSAGE ACTION
# ==========================================================

def send_message_action(
    message_entry,
    messages_box,
    current_user,
    selected_user
):
    """
    Sends a new message.
    """


    message = message_entry.get().strip()



    success, result = send_chat_message(
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
            messages_box,
            current_user,
            selected_user
        )



    else:


        messagebox.showerror(
            "Message Error",
            result
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
            Logged-in user.

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
        pady=20
    )



    # ======================================================
    # MESSAGE DISPLAY
    # ======================================================

    messages_box = tk.Text(
        window,
        wrap="word",
        state="disabled"
    )


    messages_box.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )



    # ======================================================
    # MESSAGE INPUT
    # ======================================================

    input_frame = ttk.Frame(
        window
    )


    input_frame.pack(
        fill="x",
        padx=20,
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
            messages_box,
            current_user,
            selected_user
        )
    )


    send_button.pack(
        side="right",
        padx=(10,0)
    )



    # ======================================================
    # INITIAL MESSAGE LOAD
    # ======================================================

    load_messages(
        messages_box,
        current_user,
        selected_user
    )