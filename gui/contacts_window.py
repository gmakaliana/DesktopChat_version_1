"""
Contacts Window

Provides the graphical interface for
managing user contacts.

Responsibilities:
- Search users.
- Add contacts.
- Display current contacts.

Business logic is handled by:
    modules/contacts/contacts.py
"""


import tkinter as tk
from tkinter import ttk, messagebox


from modules.contacts.contacts import (
    search_available_users,
    add_new_contact,
    get_user_contacts
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
# SEARCH USERS ACTION
# ==========================================================

def search_action(
    search_entry,
    results_list,
    current_user
):
    """
    Searches registered users.
    """


    keyword = search_entry.get().strip()



    if keyword == "":

        messagebox.showwarning(
            "Search",
            "Enter username or name",
        )

        return



    users = search_available_users(
        keyword
    )



    results_list.delete(
        0,
        tk.END
    )



    for user in users:


        # Prevent showing yourself

        if user["user_id"] != current_user["user_id"]:


            results_list.insert(
                tk.END,
                (
                    f"{user['user_id']} - "
                    f"{user['username']} "
                    f"({user['full_name']})"
                )
            )



# ==========================================================
# ADD CONTACT ACTION
# ==========================================================

def add_contact_action(
    results_list,
    current_user
):
    """
    Adds selected user as contact.
    """



    selected = results_list.curselection()



    if not selected:

        messagebox.showwarning(
            "Add Contact",
            "Select a user first"
        )

        return



    data = results_list.get(
        selected[0]
    )



    # Extract user ID

    friend_id = int(
        data.split("-")[0]
    )



    success, message = add_new_contact(
        current_user["user_id"],
        friend_id
    )



    if success:

        messagebox.showinfo(
            "Success",
            message
        )

    else:

        messagebox.showerror(
            "Error",
            message
        )



# ==========================================================
# LOAD CONTACTS
# ==========================================================

def load_contacts(
    contacts_list,
    current_user
):
    """
    Displays existing contacts.
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
            (
                f"{contact['username']} "
                f"({contact['full_name']})"
            )
        )



# ==========================================================
# OPEN CONTACT WINDOW
# ==========================================================

def open_contacts_window(
    parent,
    current_user
):
    """
    Opens contact management window.

    Args:
        parent:
            Home window.

        current_user:
            Logged-in user.
    """


    window = tk.Toplevel(
        parent
    )


    window.title(
        "Contacts"
    )


    window.resizable(
        False,
        False
    )


    window.configure(
        background=BACKGROUND
    )



    center_window(
        window,
        600,
        500
    )



    # Keep above home window

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
    # TITLE
    # ======================================================

    title = tk.Label(
        window,
        text="Manage Contacts",
        font=TITLE_FONT,
        bg=BACKGROUND
    )


    title.pack(
        pady=20
    )



    # ======================================================
    # SEARCH AREA
    # ======================================================

    search_frame = ttk.Frame(
        window
    )


    search_frame.pack(
        pady=10
    )



    search_entry = ttk.Entry(
        search_frame,
        width=35
    )


    search_entry.pack(
        side="left",
        padx=5
    )



    search_button = ttk.Button(
        search_frame,
        text="Search",
        command=lambda:

        search_action(
            search_entry,
            results_list,
            current_user
        )
    )


    search_button.pack(
        side="left"
    )



    # ======================================================
    # SEARCH RESULTS
    # ======================================================

    results_frame = ttk.LabelFrame(
        window,
        text="Search Results"
    )


    results_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )



    results_list = tk.Listbox(
        results_frame
    )


    results_list.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )



    # ======================================================
    # ADD BUTTON
    # ======================================================

    add_button = ttk.Button(
        window,
        text="Add Selected Contact",
        command=lambda:

        add_contact_action(
            results_list,
            current_user
        )
    )


    add_button.pack(
        pady=10
    )



    # ======================================================
    # CURRENT CONTACTS
    # ======================================================

    contacts_frame = ttk.LabelFrame(
        window,
        text="My Contacts"
    )


    contacts_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )



    contacts_list = tk.Listbox(
        contacts_frame
    )


    contacts_list.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )



    load_contacts(
        contacts_list,
        current_user
    )