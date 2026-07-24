"""
Home Window

Main interface of the Desktop Chat System.

Responsibilities:
- Display logged-in user.
- Display contacts.
- Open chat window.
- Open contact management.
- Handle logout.

Business logic is handled by:
    modules/
"""


import tkinter as tk
from tkinter import ttk


from datetime import datetime


from modules.contacts.contacts import (
    get_user_contacts
)


from gui.chat_window import (
    open_chat_window
)


from gui.contacts_window import (
    open_contacts_window
)


from database.queries import (
    update_user_status,
    update_last_seen
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
# LOGOUT
# ==========================================================

def logout(
    window,
    user,
    login_window
):
    """
    Logs out the current user.

    Actions:
    - Change status to Offline.
    - Save last seen.
    - Close home window.
    - Return to login.
    """


    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    update_user_status(
        user["user_id"],
        "Offline"
    )


    update_last_seen(
        user["user_id"],
        current_time
    )


    close_window(
        window
    )


    login_window.deiconify()



# ==========================================================
# LOAD CONTACTS
# ==========================================================

def load_contacts(
    contacts_list,
    current_user
):
    """
    Loads user's contacts into listbox.
    """


    contacts_list.delete(
        0,
        tk.END
    )


    contacts = get_user_contacts(
        current_user["user_id"]
    )



    if not contacts:


        contacts_list.insert(
            tk.END,
            "No contacts"
        )


        return



    for contact in contacts:


        contacts_list.insert(
            tk.END,
            contact
        )



# ==========================================================
# OPEN SELECTED CHAT
# ==========================================================

def open_selected_chat(
    contacts_list,
    current_user,
    parent
):
    """
    Opens chat with selected contact.
    """


    selected = contacts_list.curselection()



    if not selected:

        return



    contact = contacts_list.get(
        selected[0]
    )



    # Ignore empty list message

    if contact == "No contacts":

        return



    open_chat_window(
        parent,
        current_user,
        contact
    )



# ==========================================================
# OPEN HOME WINDOW
# ==========================================================

def open_home_window(
    user,
    login_window
):
    """
    Opens main application window.
    """


    update_user_status(
        user["user_id"],
        "Online"
    )



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
        900,
        600
    )



    window.protocol(
        "WM_DELETE_WINDOW",
        lambda:

        logout(
            window,
            user,
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
        text=(
            f"Welcome, "
            f"{user['full_name']}"
        ),
        font=NORMAL_FONT,
        bg=BACKGROUND
    )


    username_label.pack(
        side="left"
    )



    # Manage Contacts Button

    contacts_button = ttk.Button(
        header,
        text="Contacts",
        command=lambda:

        open_contacts_window(
            window,
            user
        )
    )


    contacts_button.pack(
        side="right",
        padx=10
    )



    logout_button = ttk.Button(
        header,
        text="Logout",
        command=lambda:

        logout(
            window,
            user,
            login_window
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
    # CONTACT LIST
    # ======================================================


    contacts_frame = ttk.LabelFrame(
        main_frame,
        text="My Contacts"
    )


    contacts_frame.pack(
        side="left",
        fill="y",
        padx=(0,10)
    )



    contacts_list = tk.Listbox(
        contacts_frame,
        width=30
    )


    contacts_list.pack(
        fill="y",
        padx=10,
        pady=10
    )



    load_contacts(
        contacts_list,
        user
    )



    contacts_list.bind(
        "<Double-Button-1>",
        lambda event:

        open_selected_chat(
            contacts_list,
            user,
            window
        )
    )



    # ======================================================
    # CHAT INFORMATION AREA
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



    message = tk.Label(
        chat_frame,
        text=(
            "Select a contact "
            "to start chatting"
        ),
        font=NORMAL_FONT,
        bg=BACKGROUND
    )


    message.pack(
        expand=True
    )