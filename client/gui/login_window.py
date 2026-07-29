"""
Login Window

The first window of the Desktop Chat System.

Responsibilities:
- Display login interface.
- Authenticate users.
- Connect to WebSocket server.
- Open registration window.
- Open home window after successful login.

The Login Window is the main application window.
Closing it exits the entire application.
"""


import tkinter as tk
from tkinter import ttk, messagebox



from auth.login import login_user



from gui.register_window import open_register_window



from utils.window_utils import (
    center_window,
    exit_application
)



from utils.gui_theme import (
    BACKGROUND,
    TITLE_FONT,
    NORMAL_FONT
)





# ==========================================================
# NETWORK IMPORTS
# ==========================================================

from modules.network.connection import (
    connect_to_server,
    send_event
)



from modules.network.websocket_client import (
    client
)









# ==========================================================
# LOGIN ACTION
# ==========================================================

def login_action(
    username_entry,
    password_entry,
    window
):
    """
    Handles login button click.

    Flow:

    1. Get credentials.
    2. Authenticate user.
    3. Connect WebSocket.
    4. Save user session.
    5. Send login event.
    6. Open home window.
    """


    username = username_entry.get().strip()

    password = password_entry.get().strip()



    success, result = login_user(

        username,

        password

    )





    if success:



        # ==================================================
        # CONNECT TO SERVER
        # ==================================================

        connected = connect_to_server()



        if not connected:


            messagebox.showerror(

                "Connection Error",

                "Could not connect to chat server.",

                parent=window

            )


            return







        # ==================================================
        # SAVE USER SESSION
        # Used by reconnect system
        # ==================================================

        client.set_user(

            result["user_id"]

        )








        # ==================================================
        # SEND LOGIN EVENT
        # ==================================================

        sent = send_event(

            {

                "event":

                "login",


                "user_id":

                result["user_id"]

            }

        )





        if not sent:


            messagebox.showerror(

                "Server Error",

                "Could not register user online.",

                parent=window

            )


            client.disconnect()


            return







        # ==================================================
        # LOGIN SUCCESS
        # ==================================================

        messagebox.showinfo(

            "Login Successful",

            f"Welcome {result['full_name']}",

            parent=window

        )







        # ==================================================
        # CLEAR FIELDS
        # ==================================================

        username_entry.delete(

            0,

            tk.END

        )


        password_entry.delete(

            0,

            tk.END

        )







        # ==================================================
        # HIDE LOGIN WINDOW
        # ==================================================

        window.withdraw()







        # ==================================================
        # OPEN HOME WINDOW
        # ==================================================

        from gui.home_window import open_home_window



        open_home_window(

            result,

            window

        )









    else:



        messagebox.showerror(

            "Login Failed",

            result,

            parent=window

        )









# ==========================================================
# REGISTER ACTION
# ==========================================================

def register_action(parent):
    """
    Opens registration window.
    """


    open_register_window(

        parent

    )









# ==========================================================
# LOGIN WINDOW
# ==========================================================

def open_login_window():
    """
    Creates main login window.

    Only place where tk.Tk()
    is created.
    """



    window = tk.Tk()



    window.title(

        "Desktop Chat System"

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

        450,

        350

    )







    # ======================================================
    # CLOSE APPLICATION
    # ======================================================

    window.protocol(

        "WM_DELETE_WINDOW",

        lambda:

        exit_application(window)

    )







    # ======================================================
    # TITLE
    # ======================================================

    title_label = tk.Label(

        window,

        text="Desktop Chat System",

        font=TITLE_FONT,

        bg=BACKGROUND

    )


    title_label.pack(

        pady=(25,20)

    )







    # ======================================================
    # USERNAME
    # ======================================================

    username_label = tk.Label(

        window,

        text="Username",

        font=NORMAL_FONT,

        bg=BACKGROUND

    )


    username_label.pack(

        anchor="w",

        padx=50

    )



    username_entry = ttk.Entry(

        window,

        width=35

    )


    username_entry.pack(

        padx=50,

        pady=(5,15)

    )







    # ======================================================
    # PASSWORD
    # ======================================================

    password_label = tk.Label(

        window,

        text="Password",

        font=NORMAL_FONT,

        bg=BACKGROUND

    )


    password_label.pack(

        anchor="w",

        padx=50

    )



    password_entry = ttk.Entry(

        window,

        width=35,

        show="*"

    )


    password_entry.pack(

        padx=50,

        pady=(5,20)

    )







    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = ttk.Frame(

        window

    )


    button_frame.pack(

        pady=10

    )







    # ======================================================
    # LOGIN BUTTON
    # ======================================================

    login_button = ttk.Button(

        button_frame,

        text="Login",

        command=lambda:

        login_action(

            username_entry,

            password_entry,

            window

        )

    )


    login_button.pack(

        side="left",

        padx=10

    )







    # ======================================================
    # REGISTER BUTTON
    # ======================================================

    register_button = ttk.Button(

        button_frame,

        text="Register",

        command=lambda:

        register_action(

            window

        )

    )


    register_button.pack(

        side="left",

        padx=10

    )







    window.mainloop()

    