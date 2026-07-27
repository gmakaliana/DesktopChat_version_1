"""
Contacts Window

Allows users to:

- Search for users.
- Add contacts.
- View contacts.
- Remove contacts.
- View contact count.

Business logic:
    modules/contacts/contacts.py
"""


import tkinter as tk
from tkinter import ttk, messagebox



from modules.contacts.contacts import (

    search_available_users,

    add_new_contact,

    get_user_contacts,

    remove_existing_contact,

    get_user_contact_count

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
    results_tree,
    results_objects,
    current_user
):


    keyword = search_entry.get().strip()


    results_tree.delete(
        *results_tree.get_children()
    )


    results_objects.clear()



    users = search_available_users(
        keyword,
        current_user["user_id"]
    )



    for user in users:


        results_objects.append(
            user
        )



        status = user["status"]



        results_tree.insert(
            "",
            tk.END,
            values=(

                user["username"],

                user["full_name"],

                status

            )
        )



# ==========================================================
# ADD CONTACT
# ==========================================================

def add_contact_action(
    results_tree,
    results_objects,
    current_user,
    contacts_tree,
    count_label
):


    selected = results_tree.selection()



    if not selected:


        messagebox.showwarning(
            "No Selection",
            "Select a user first."
        )


        return



    index = results_tree.index(
        selected[0]
    )



    user = results_objects[index]



    success = add_new_contact(

        current_user["user_id"],

        user["user_id"]

    )



    if success:


        messagebox.showinfo(
            "Success",
            "Contact added successfully."
        )


        load_contacts(
            contacts_tree,
            current_user,
            count_label
        )



    else:


        messagebox.showerror(
            "Failed",
            "Could not add contact."
        )





# ==========================================================
# LOAD CONTACTS
# ==========================================================

def load_contacts(
    contacts_tree,
    current_user,
    count_label
):


    contacts_tree.delete(
        *contacts_tree.get_children()
    )



    contacts = get_user_contacts(
        current_user["user_id"]
    )



    for contact in contacts:


        contacts_tree.insert(
            "",
            tk.END,
            values=(

                contact["username"],

                contact["full_name"],

                contact["status"],

                contact["last_seen"]

            )
        )



    count = get_user_contact_count(
        current_user["user_id"]
    )



    count_label.config(
        text=f"Contacts: {count}"
    )

# ==========================================================
# REMOVE CONTACT
# ==========================================================

def remove_contact_action(
    contacts_tree,
    current_user,
    count_label
):
    """
    Removes a contact after confirmation.
    """


    selected = contacts_tree.selection()



    if not selected:


        messagebox.showwarning(
            "No Selection",
            "Select a contact first."
        )


        return



    values = contacts_tree.item(
        selected[0]
    )["values"]



    username = values[0]



    contacts = get_user_contacts(
        current_user["user_id"]
    )



    selected_contact = None



    for contact in contacts:


        if contact["username"] == username:

            selected_contact = contact

            break



    if selected_contact is None:

        return



    # ======================================================
    # CONFIRM REMOVE
    # ======================================================

    confirm = messagebox.askyesno(
        "Remove Contact",
        (
            f"Are you sure you want to remove "
            f"{selected_contact['full_name']}?"
        )
    )



    if not confirm:

        return



    # ======================================================
    # REMOVE CONTACT
    # ======================================================

    success = remove_existing_contact(

        current_user["user_id"],

        selected_contact["user_id"]

    )



    if success:


        messagebox.showinfo(
            "Removed",
            "Contact removed successfully."
        )


        load_contacts(
            contacts_tree,
            current_user,
            count_label
        )



    else:


        messagebox.showerror(
            "Error",
            "Could not remove contact."
        )



# ==========================================================
# OPEN CONTACT WINDOW
# ==========================================================

def open_contacts_window(
    parent,
    current_user
):


    window = tk.Toplevel(
        parent
    )



    window.title(
        "Contacts Management"
    )



    window.geometry(
        "850x750"
    )



    window.configure(
        background=BACKGROUND
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



    center_window(
        window,
        850,
        750
    )



    # ======================================================
    # TITLE
    # ======================================================


    title = tk.Label(

        window,

        text="Contacts",

        font=TITLE_FONT,

        bg=BACKGROUND

    )


    title.pack(
        pady=15
    )



    # ======================================================
    # SEARCH SECTION
    # ======================================================


    search_frame = ttk.LabelFrame(

        window,

        text="Search Users"

    )


    search_frame.pack(

        fill="x",

        padx=20,

        pady=10

    )



    search_entry = ttk.Entry(
        search_frame,
        width=40
    )


    search_entry.pack(
        side="left",
        padx=10,
        pady=10
    )



    results_objects = []



    results_tree = ttk.Treeview(

        window,

        columns=(

            "username",

            "name",

            "status"

        ),

        show="headings",

        height=6

    )


    for col in results_tree["columns"]:


        results_tree.heading(
            col,
            text=col.title()
        )



    results_tree.pack(
        fill="x",
        padx=20
    )



    ttk.Button(

        search_frame,

        text="Search",

        command=lambda:

        search_action(

            search_entry,

            results_tree,

            results_objects,

            current_user

        )

    ).pack(
        side="right",
        padx=10
    )

    ttk.Button(

        window,

        text="Add Contact",

        command=lambda:

        add_contact_action(

            results_tree,

            results_objects,

            current_user,

            contacts_tree,

            count_label

        )

    ).pack(
        pady=10
    )

    # ======================================================
    # MY CONTACTS
    # ======================================================


    contacts_frame = ttk.LabelFrame(

        window,

        text="My Contacts"

    )


    contacts_frame.pack(

        fill="both",

        padx=20,

        pady=10

    )



    count_label = ttk.Label(
        contacts_frame,
        text="Contacts: 0"
    )


    count_label.pack(
        anchor="w"
    )



    contacts_tree = ttk.Treeview(

        contacts_frame,

        columns=(

            "username",

            "name",

            "status",

            "last_seen"

        ),

        show="headings",

        height=12

    )

    

    for col in contacts_tree["columns"]:


        contacts_tree.heading(
            col,
            text=col.title()
        )



    contacts_tree.pack(

        fill="both",

        expand=True

    )


    

    # ======================================================
    # ACTION BUTTONS
    # ======================================================


    button_frame = ttk.Frame(
        window
    )


    button_frame.pack(
        side="bottom",
        pady=10
    )



    ttk.Button(

        button_frame,

        text="Remove Contact",

        command=lambda:

        remove_contact_action(

            contacts_tree,

            current_user,

            count_label

        )

    ).pack(
        side="left",
        padx=10
    )



    ttk.Button(

        button_frame,

        text="Refresh",

        command=lambda:

        load_contacts(

            contacts_tree,

            current_user,

            count_label

        )

    ).pack(
        side="left",
        padx=10
    )



    # Initial load

    load_contacts(

        contacts_tree,

        current_user,

        count_label

    )



    search_entry.focus()