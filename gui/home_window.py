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


from modules.contacts.contacts import (
    get_user_contacts
)


from gui.chat_window import (
    open_chat_window
)


from gui.contacts_window import (
    open_contacts_window
)


from modules.users.status import (
    set_offline
)


from utils.window_utils import (
    center_window,
    close_window
)


from utils.gui_theme import (
    BACKGROUND,
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
    - Update last seen.
    - Close home window.
    - Return to login window.
    """


    set_offline(
        user["user_id"]
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
    current_user,
    contact_objects
):
    """
    Loads user's contacts into listbox.
    """


    contacts_list.delete(
        0,
        tk.END
    )


    contact_objects.clear()



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


        contact_objects.append(
            contact
        )


        contacts_list.insert(
            tk.END,
            f"{contact['username']} "
            f"({contact['full_name']})"
        )



# ==========================================================
# OPEN SELECTED CHAT
# ==========================================================

def open_selected_chat(
    contacts_list,
    contact_objects,
    current_user,
    parent
):
    """
    Opens chat with selected contact.
    """


    selected = contacts_list.curselection()



    if not selected:

        return



    contact = contact_objects[
        selected[0]
    ]



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
    Opens the main application window.
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
        900,
        600
    )



    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

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



    # ======================================================
    # CONTACT MANAGEMENT BUTTON
    # ======================================================


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



    # ======================================================
    # LOGOUT BUTTON
    # ======================================================


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



    contact_objects = []



    load_contacts(
        contacts_list,
        user,
        contact_objects
    )



    contacts_list.bind(
        "<Double-Button-1>",
        lambda event:

        open_selected_chat(
            contacts_list,
            contact_objects,
            user,
            window
        )
    )



    # ======================================================
    # CHAT AREA
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