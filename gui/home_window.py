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
    set_offline,
    update_activity
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
    contacts_table,
    current_user,
    contact_objects
):
    """
    Loads the user's contacts into the Treeview.
    """

    # ----------------------------------------------
    # Clear previous rows
    # ----------------------------------------------

    for item in contacts_table.get_children():

        contacts_table.delete(item)

    contact_objects.clear()

    contacts = get_user_contacts(
        current_user["user_id"]
    )

    if not contacts:

        contacts_table.insert(
            "",
            tk.END,
            values=(
                "⚪",
                "No contacts",
                "",
                ""
            )
        )

        return

    for contact in contacts:

        contact_objects.append(contact)

        status_icon = (
            "🟢"
            if contact["status"] == "Online"
            else "⚪"
        )

        last_seen = (
            contact["last_seen"]
            if contact["last_seen"]
            else "-"
        )

        contacts_table.insert(
            "",
            tk.END,
            values=(
                status_icon,
                contact["full_name"],
                contact["username"],
                last_seen
            )
        )



# ==========================================================
# REFRESH CONTACTS
# ==========================================================

def refresh_contact_list(
    window,
    contacts_table,
    current_user,
    contact_objects
):
    """
    Refreshes the contact list every 5 seconds.

    This keeps Online/Offline status and
    Last Seen information up to date.
    """

    # ----------------------------------------------
    # Update this user's activity timestamp
    # ----------------------------------------------

    update_activity(
        current_user["user_id"]
    )

    # ----------------------------------------------
    # Reload contacts from database
    # ----------------------------------------------

    load_contacts(
        contacts_table,
        current_user,
        contact_objects
    )

    # ----------------------------------------------
    # Schedule the next refresh
    # ----------------------------------------------

    window.after(
        5000,
        lambda:
        refresh_contact_list(
            window,
            contacts_table,
            current_user,
            contact_objects
        )
    )



# ==========================================================
# OPEN SELECTED CHAT
# ==========================================================

def open_selected_chat(
    contacts_table,
    contact_objects,
    current_user,
    parent
):
    """
    Opens a chat window for the selected contact.
    """

    selected = contacts_table.selection()

    if not selected:

        return

    index = contacts_table.index(
        selected[0]
    )

    # Ignore placeholder row

    if index >= len(contact_objects):

        return

    contact = contact_objects[index]

    open_chat_window(
        parent,
        current_user,
        contact
    )



# ==========================================================
# HOME WINDOW
# ==========================================================

def open_home_window(
    user,
    login_window
):
    """
    Opens the main application window.
    """

    # ---------- Part 2 continues ----------

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
        1000,
        650
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
        text=f"Welcome, {user['full_name']}",
        font=NORMAL_FONT,
        bg=BACKGROUND
    )

    username_label.pack(
        side="left"
    )

    # ------------------------------------------------------
    # CONTACTS BUTTON
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # LOGOUT BUTTON
    # ------------------------------------------------------

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
    # CONTACTS PANEL
    # ======================================================

    contacts_frame = ttk.LabelFrame(
        main_frame,
        text="My Contacts"
    )

    contacts_frame.pack(
        side="left",
        fill="y",
        padx=(0, 10)
    )

    # ------------------------------------------------------
    # TREEVIEW
    # ------------------------------------------------------

    columns = (
        "status",
        "name",
        "username",
        "last_seen"
    )

    contacts_table = ttk.Treeview(
        contacts_frame,
        columns=columns,
        show="headings",
        height=22
    )

    contacts_table.heading(
        "status",
        text=""
    )

    contacts_table.heading(
        "name",
        text="Name"
    )

    contacts_table.heading(
        "username",
        text="Username"
    )

    contacts_table.heading(
        "last_seen",
        text="Last Seen"
    )

    contacts_table.column(
        "status",
        width=45,
        anchor="center"
    )

    contacts_table.column(
        "name",
        width=180
    )

    contacts_table.column(
        "username",
        width=140
    )

    contacts_table.column(
        "last_seen",
        width=170
    )

    scrollbar = ttk.Scrollbar(
        contacts_frame,
        orient="vertical",
        command=contacts_table.yview
    )

    contacts_table.configure(
        yscrollcommand=scrollbar.set
    )

    contacts_table.pack(
        side="left",
        padx=(10, 0),
        pady=10,
        fill="y"
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10,
        padx=(0, 10)
    )

    # ------------------------------------------------------
    # CONTACT DATA
    # ------------------------------------------------------

    contact_objects = []

    load_contacts(
        contacts_table,
        user,
        contact_objects
    )

    # ------------------------------------------------------
    # AUTOMATIC REFRESH
    # ------------------------------------------------------

    refresh_contact_list(
        window,
        contacts_table,
        user,
        contact_objects
    )

    # ------------------------------------------------------
    # DOUBLE CLICK TO CHAT
    # ------------------------------------------------------

    contacts_table.bind(
        "<Double-1>",
        lambda event:
        open_selected_chat(
            contacts_table,
            contact_objects,
            user,
            window
        )
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

    message = tk.Label(
        chat_frame,
        text=(
            "Double-click a contact to "
            "start chatting."
        ),
        font=NORMAL_FONT,
        bg=BACKGROUND
    )

    message.pack(
        expand=True
    )