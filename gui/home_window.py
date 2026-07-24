"""
Home Window

Main interface of the Desktop Chat System.

This window appears after successful login.

Responsibilities:
- Display logged-in user information.
- Display contacts area.
- Display chat area.
- Handle logout.

Future:
- Load contacts from database.
- Real-time messaging using WebSockets.
- Image sharing.
"""


import tkinter as tk
from tkinter import ttk


from utils.window_utils import (
    center_window,
    close_window
)


from utils.gui_theme import (
    BACKGROUND,
    TITLE_FONT,
    HEADER_FONT,
    NORMAL_FONT
)



# ==========================================================
# LOGOUT
# ==========================================================

def logout(window, login_window, user_id):
    """
    Logs the user out.

    Future:
    - Update user status to Offline.
    - Close WebSocket connection.
    """


    # Close home window

    window.destroy()



    # Show login window again

    login_window.deiconify()



# ==========================================================
# CLOSE HOME WINDOW
# ==========================================================

def close_home_window(window, login_window):
    """
    Handles X button.

    Does not close the whole application.
    Returns user to login screen.
    """


    window.destroy()


    login_window.deiconify()



# ==========================================================
# HOME WINDOW
# ==========================================================

def open_home_window(user, login_window):
    """
    Opens the main chat window.

    Args:
        user:
            Logged-in user database row.

        login_window:
            Original login window.
    """


    window = tk.Toplevel(
        login_window
    )



    window.title(
        "Desktop Chat System"
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
        1100,
        700
    )



    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    window.protocol(
        "WM_DELETE_WINDOW",
        lambda:

        close_home_window(
            window,
            login_window
        )
    )



    # ======================================================
    # HEADER
    # ======================================================

    header = ttk.Frame(
        window
    )


    header.pack(
        fill="x",
        padx=15,
        pady=15
    )



    username_label = tk.Label(
        header,
        text=f"Welcome, {user['full_name']}",
        font=HEADER_FONT,
        bg=BACKGROUND
    )


    username_label.pack(
        side="left"
    )



    logout_button = ttk.Button(
        header,
        text="Logout",
        command=lambda:

        logout(
            window,
            login_window,
            user["user_id"]
        )
    )


    logout_button.pack(
        side="right"
    )



    # ======================================================
    # MAIN AREA
    # ======================================================

    main_frame = ttk.Frame(
        window
    )


    main_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )



    # ======================================================
    # CONTACTS PANEL
    # ======================================================

    contacts_frame = ttk.LabelFrame(
        main_frame,
        text="Contacts"
    )


    contacts_frame.pack(
        side="left",
        fill="y",
        padx=(0,15)
    )



    contacts_list = tk.Listbox(
        contacts_frame,
        width=30,
        font=NORMAL_FONT
    )


    contacts_list.pack(
        fill="y",
        padx=10,
        pady=10
    )


    contacts_list.insert(
        tk.END,
        "No contacts available"
    )



    # ======================================================
    # CHAT PANEL
    # ======================================================

    chat_frame = ttk.LabelFrame(
        main_frame,
        text="Chat"
    )


    chat_frame.pack(
        side="right",
        fill="both",
        expand=True
    )



    messages_box = tk.Text(
        chat_frame,
        wrap="word",
        state="disabled",
        font=NORMAL_FONT
    )


    messages_box.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )



    # ======================================================
    # MESSAGE INPUT
    # ======================================================

    input_frame = ttk.Frame(
        chat_frame
    )


    input_frame.pack(
        fill="x",
        padx=10,
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
        text="Send"
    )


    send_button.pack(
        side="right",
        padx=10
    )