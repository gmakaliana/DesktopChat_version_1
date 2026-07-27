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
from tkinter import ttk

from modules.chat.chat import (
    send_chat_message,
    get_display_messages,
    mark_conversation_read
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
    Loads messages as chat bubbles.
    """


    chat_box.config(
        state="normal"
    )


    chat_box.delete(
        "1.0",
        tk.END
    )

    mark_conversation_read(
        current_user["user_id"],
        selected_user["user_id"]
    )

    messages = get_display_messages(
        current_user["user_id"],
        selected_user["user_id"]
    )

    for message in messages:

        # --------------------------------------------------
        # Current user's message
        # --------------------------------------------------

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

            if message["is_read"]:

                status = "✓✓ Read"

            else:

                status = "✓ Sent"

            chat_box.insert(
                tk.END,
                f"{message['time']}   {status}\n",
                "time"
            )

        # --------------------------------------------------
        # Other user's message
        # --------------------------------------------------

        else:


            chat_box.insert(
                tk.END,
                "\n"
                + message["sender"]
                + "\n",
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
# AUTO REFRESH CHAT
# ==========================================================

def refresh_chat(
    window,
    chat_box,
    current_user,
    selected_user
):
    """
    Automatically refreshes
    conversation every 2 seconds.
    """


    # Stop refreshing if window closed

    if not window.winfo_exists():

        return



    load_messages(
        chat_box,
        current_user,
        selected_user
    )



    # Run again after 2 seconds

    window.after(
        2000,
        lambda:

        refresh_chat(
            window,
            chat_box,
            current_user,
            selected_user
        )
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


        message_entry.delete(
            0,
            tk.END
        )


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
    # CHAT DISPLAY WITH SCROLLBAR
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

    # Message display

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

    # Vertical scrollbar

    scrollbar = ttk.Scrollbar(
        chat_frame,
        orient="vertical",
        command=chat_box.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # Connect scrollbar to text box

    chat_box.configure(
        yscrollcommand=scrollbar.set
    )

    # ======================================================
    # CHAT BUBBLE FORMATTING
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
    # ENTER SEND
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
            selected_user
        )
    )

    message_entry.focus()

