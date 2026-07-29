"""
Home Window

Main interface of the Desktop Chat System.

Responsibilities:
- Display logged-in user.
- Display contacts.
- Open chat window.
- Handle logout.
- Receive real-time WebSocket events.

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
# WEBSOCKET IMPORTS
# ==========================================================

from modules.network.connection import (
    register_server_event,
    send_event
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
    - Notify server.
    - Close home window.
    - Return to login.
    """


    send_event(

        {

            "event":
            "logout",

            "user_id":
            user["user_id"]

        }

    )



    close_window(
        window
    )



    login_window.deiconify()







# ==========================================================
# WEBSOCKET EVENT HANDLERS
# ==========================================================


def handle_user_online(data):
    """
    Handles user_online event.
    """

    print(
        "User online:",
        data.get("user_id")
    )




def handle_user_offline(data):
    """
    Handles user_offline event.
    """

    print(
        "User offline:",
        data.get("user_id")
    )




def handle_new_message(data):
    """
    Handles incoming messages.
    """

    print(
        "New message:",
        data
    )




def handle_notification(data):
    """
    Handles notifications.
    """

    print(
        "Notification:",
        data
    )






def register_home_events():
    """
    Registers WebSocket events
    required by Home Window.
    """



    register_server_event(

        "user_online",

        handle_user_online

    )



    register_server_event(

        "user_offline",

        handle_user_offline

    )



    register_server_event(

        "message",

        handle_new_message

    )



    register_server_event(

        "notification",

        handle_notification

    )









# ==========================================================
# LOAD CONTACTS
# ==========================================================

def load_contacts(
    contacts_table,
    current_user,
    contact_objects
):
    """
    Loads contacts from database.

    Temporary:
    This will later be replaced
    completely by server data.
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



        status_icon = (

            "🟢"

            if contact["status"] == "Online"

            else "⚪"

        )



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
# OPEN SELECTED CHAT
# ==========================================================

def open_selected_chat(
    contacts_table,
    contact_objects,
    current_user,
    parent
):
    """
    Opens chat window.
    """


    selected = contacts_table.selection()



    if not selected:

        return



    index = contacts_table.index(

        selected[0]

    )



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


    # Register WebSocket events

    register_home_events()



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







    contact_objects = []



    load_contacts(

        contacts_table,

        user,

        contact_objects

    )



    # ======================================================
    # OLD POLLING DISABLED
    #
    # WebSocket events now handle:
    # - online/offline changes
    # - notifications
    # - messages
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