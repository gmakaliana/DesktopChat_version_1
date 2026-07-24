"""
Registration Window

Provides the graphical interface for creating
new user accounts.

This module only handles GUI operations.

Registration logic is handled by:
    auth/register.py
"""


import tkinter as tk
from tkinter import ttk, messagebox


from auth.register import register_user


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
# REGISTER ACTION
# ==========================================================

def register_action(
    username_entry,
    password_entry,
    fullname_entry,
    window
):
    """
    Handles registration button click.
    """


    username = username_entry.get().strip()

    password = password_entry.get().strip()

    full_name = fullname_entry.get().strip()



    success, message = register_user(
        username,
        password,
        full_name
    )



    if success:


        messagebox.showinfo(
            "Registration Successful",
            message,
            parent=window
        )



        # Clear fields after successful registration

        fullname_entry.delete(
            0,
            tk.END
        )


        username_entry.delete(
            0,
            tk.END
        )


        password_entry.delete(
            0,
            tk.END
        )



    else:


        messagebox.showerror(
            "Registration Failed",
            message,
            parent=window
        )



# ==========================================================
# LOGIN ACTION
# ==========================================================

def login_action(
    window,
    parent
):
    """
    Returns user to login window.
    """

    # Close registration window

    close_window(
        window
    )


    # Show login window again

    parent.deiconify()



# ==========================================================
# OPEN REGISTER WINDOW
# ==========================================================

def open_register_window(parent):
    """
    Opens registration window.

    Args:
        parent:
            Login window.
    """


    window = tk.Toplevel(
        parent
    )


    window.title(
        "Create Account"
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
        420
    )



    # Keep above login window

    window.transient(
        parent
    )



    # Block interaction with parent

    window.grab_set()



    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    window.protocol(
        "WM_DELETE_WINDOW",
        lambda:

        close_window(window)
    )



    # ======================================================
    # TITLE
    # ======================================================

    title_label = tk.Label(
        window,
        text="Create New Account",
        font=TITLE_FONT,
        bg=BACKGROUND
    )


    title_label.pack(
        pady=(25,20)
    )



    # ======================================================
    # FULL NAME
    # ======================================================

    fullname_label = tk.Label(
        window,
        text="Full Name",
        font=NORMAL_FONT,
        bg=BACKGROUND
    )


    fullname_label.pack(
        anchor="w",
        padx=50
    )


    fullname_entry = ttk.Entry(
        window,
        width=35
    )


    fullname_entry.pack(
        padx=50,
        pady=(5,15)
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
    # BUTTON AREA
    # ======================================================

    button_frame = ttk.Frame(
        window
    )


    button_frame.pack(
        pady=10
    )



    # ======================================================
    # TOP BUTTON ROW
    # ======================================================

    top_button_frame = ttk.Frame(
        button_frame
    )


    top_button_frame.pack()



    # ======================================================
    # REGISTER BUTTON
    # ======================================================

    register_button = ttk.Button(
        top_button_frame,
        text="Register",
        command=lambda:

        register_action(
            username_entry,
            password_entry,
            fullname_entry,
            window
        )
    )


    register_button.pack(
        side="left",
        padx=10
    )



    # ======================================================
    # LOGIN BUTTON
    # ======================================================

    login_button = ttk.Button(
        top_button_frame,
        text="Login",
        command=lambda:

        login_action(
            window,
            parent
        )
    )


    login_button.pack(
        side="left",
        padx=10
    )



   