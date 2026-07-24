"""
Contacts Window

Allows users to:
- Search for users.
- Add contacts.
- View search results.

Business logic:
    modules/contacts/contacts.py
"""


import tkinter as tk
from tkinter import ttk, messagebox



from modules.contacts.contacts import (
    search_available_users,
    add_new_contact
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
# SEARCH USERS
# ==========================================================

def search_action(
    search_entry,
    results_list,
    results_objects,
    current_user
):
    """
    Searches users.
    """


    keyword = search_entry.get().strip()



    results_list.delete(
        0,
        tk.END
    )


    results_objects.clear()



    users = search_available_users(
        keyword,
        current_user["user_id"]
    )



    if not users:


        results_list.insert(
            tk.END,
            "No users found"
        )


        return




    for user in users:


        results_objects.append(
            user
        )



        if user["status"] == "Online":

            icon = "🟢"

        else:

            icon = "⚪"



        display = (

            f"{icon} "

            f"{user['full_name']} "

            f"({user['username']})"

        )


        results_list.insert(
            tk.END,
            display
        )





# ==========================================================
# ADD CONTACT
# ==========================================================

def add_contact_action(
    results_list,
    results_objects,
    current_user
):
    """
    Adds selected search result
    as contact.
    """


    selected = results_list.curselection()



    if not selected:


        messagebox.showwarning(
            "No Selection",
            "Please select a user first."
        )


        return



    user = results_objects[
        selected[0]
    ]



    success = add_new_contact(
        current_user["user_id"],
        user["user_id"]
    )



    if success:


        messagebox.showinfo(
            "Success",
            f"{user['full_name']} added as contact."
        )


    else:


        messagebox.showerror(
            "Failed",
            "User is already a contact."
        )





# ==========================================================
# OPEN CONTACT WINDOW
# ==========================================================

def open_contacts_window(
    parent,
    current_user
):
    """
    Opens contacts management window.
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
        550,
        500
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
    # TITLE
    # ======================================================


    title = tk.Label(
        window,
        text="Search Users",
        font=TITLE_FONT,
        bg=BACKGROUND
    )


    title.pack(
        pady=(20,15)
    )



    # ======================================================
    # SEARCH AREA
    # ======================================================


    search_frame = ttk.Frame(
        window
    )


    search_frame.pack(
        fill="x",
        padx=30
    )



    search_entry = ttk.Entry(
        search_frame,
        width=35
    )


    search_entry.pack(
        side="left"
    )



    # Results storage

    results_objects = []



    results_list = tk.Listbox(
        window,
        width=55,
        height=15
    )


    results_list.pack(
        padx=30,
        pady=20
    )



    search_button = ttk.Button(
        search_frame,
        text="Search",
        command=lambda:

        search_action(
            search_entry,
            results_list,
            results_objects,
            current_user
        )
    )


    search_button.pack(
        side="right",
        padx=10
    )



    # ======================================================
    # ADD CONTACT BUTTON
    # ======================================================


    add_button = ttk.Button(
        window,
        text="Add Contact",
        command=lambda:

        add_contact_action(
            results_list,
            results_objects,
            current_user
        )
    )


    add_button.pack(
        pady=10
    )



    # ======================================================
    # ENTER KEY SEARCH
    # ======================================================


    search_entry.bind(
        "<Return>",
        lambda event:

        search_action(
            search_entry,
            results_list,
            results_objects,
            current_user
        )
    )



    search_entry.focus()