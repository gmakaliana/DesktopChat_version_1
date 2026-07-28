"""
Home Window

Main interface of the Desktop Chat System.

Responsibilities:
- Display logged-in user.
- Display contacts.
- Open chat window.
- Handle logout.
- Show unread message badges.
- Show new message notifications.
- Detect contact status changes.

Business logic:
    modules/
"""


import tkinter as tk
from tkinter import ttk, messagebox



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



from modules.chat.chat import (
    get_contact_unread_count
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
    Logs out current user.

    Actions:
    - Set user offline.
    - Close home window.
    - Return to login.
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
    Loads contacts into TreeView.

    Displays:
    - Online/offline icon
    - Name
    - Username
    - Last seen
    - Unread message count
    """


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



        contact_objects.append(
            contact
        )



        # Status icon

        status_icon = (

            "🟢"

            if contact["status"] == "Online"

            else "⚪"

        )



        # Get unread messages

        unread_count = get_contact_unread_count(

            current_user["user_id"],

            contact["user_id"]

        )



        display_name = contact["full_name"]



        if unread_count > 0:


            display_name = (

                f"{display_name} ({unread_count})"

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

                display_name,

                contact["username"],

                last_seen

            )

        )







# ==========================================================
# NOTIFICATION SYSTEM
# ==========================================================

def check_notifications(
    window,
    current_user,
    notification_state
):
    """
    Checks:

    1. New unread messages
    2. Contact online/offline changes


    Runs every 5 seconds.
    """


    contacts = get_user_contacts(

        current_user["user_id"]

    )



    for contact in contacts:



        contact_id = contact["user_id"]



        current_status = contact["status"]



        current_unread = get_contact_unread_count(

            current_user["user_id"],

            contact_id

        )



        # ----------------------------------------------
        # First time loading contact
        # ----------------------------------------------

        if contact_id not in notification_state:


            notification_state[contact_id] = {


                "status": current_status,


                "unread": current_unread


            }


            continue







        old_status = notification_state[contact_id]["status"]


        old_unread = notification_state[contact_id]["unread"]







        # ==================================================
        # STATUS CHANGE
        # ==================================================

        if old_status != current_status:



            messagebox.showinfo(

                "Contact Status",

                f"{contact['full_name']} is now {current_status}"

            )








        # ==================================================
        # NEW MESSAGE
        # ==================================================

        if current_unread > old_unread:



            new_messages = (

                current_unread - old_unread

            )



            messagebox.showinfo(

                "New Message",

                f"{contact['full_name']} sent you "
                f"{new_messages} new message(s)."

            )







        notification_state[contact_id] = {


            "status": current_status,


            "unread": current_unread


        }







    window.after(

        5000,

        lambda:

        check_notifications(

            window,

            current_user,

            notification_state

        )

    )







# ==========================================================
# REFRESH CONTACT LIST
# ==========================================================

def refresh_contact_list(
    window,
    contacts_table,
    current_user,
    contact_objects
):
    """
    Automatically refreshes contacts.
    """


    update_activity(

        current_user["user_id"]

    )



    load_contacts(

        contacts_table,

        current_user,

        contact_objects

    )



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
    Opens chat window for selected contact.
    """


    selected = contacts_table.selection()



    if not selected:

        return



    index = contacts_table.index(

        selected[0]

    )



    # Ignore empty placeholder row

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
    Opens main application window.
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

        1000,

        650

    )





    # ======================================================
    # CLOSE WINDOW
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






    # CONTACTS BUTTON

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






    # LOGOUT BUTTON

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
    # CONTACT PANEL
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

        width=200

    )



    contacts_table.column(

        "username",

        width=150

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

        fill="y",

        padx=(10,0),

        pady=10

    )





    scrollbar.pack(

        side="right",

        fill="y",

        padx=(0,10),

        pady=10

    )








    # ======================================================
    # CONTACT STORAGE
    # ======================================================

    contact_objects = []



    load_contacts(

        contacts_table,

        user,

        contact_objects

    )







    # ======================================================
    # AUTO CONTACT REFRESH
    # ======================================================

    refresh_contact_list(

        window,

        contacts_table,

        user,

        contact_objects

    )








    # ======================================================
    # NOTIFICATION TRACKING
    # ======================================================

    notification_state = {}



    check_notifications(

        window,

        user,

        notification_state

    )








    # ======================================================
    # OPEN CHAT DOUBLE CLICK
    # ======================================================

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
    # CHAT INFORMATION PANEL
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

            "Double-click a contact "
            "to start chatting."

        ),

        font=NORMAL_FONT,

        bg=BACKGROUND

    )



    message.pack(

        expand=True

    )

    