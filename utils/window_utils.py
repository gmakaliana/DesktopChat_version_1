"""
Window Management Utilities

Contains common functions used by
all Tkinter windows.
"""

import tkinter as tk



# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(window, width, height):
    """
    Centers a window on screen.
    """

    screen_width = window.winfo_screenwidth()

    screen_height = window.winfo_screenheight()


    x = int(
        (screen_width - width) / 2
    )


    y = int(
        (screen_height - height) / 2
    )


    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )



# ==========================================================
# EXIT APPLICATION
# ==========================================================

def exit_application(window):
    """
    Completely closes application.
    """

    window.destroy()



# ==========================================================
# CLOSE WINDOW
# ==========================================================

def close_window(window):
    """
    Closes only current window.
    """

    window.destroy()



# ==========================================================
# OPEN CHILD WINDOW
# ==========================================================

def open_child_window(parent, title, width, height):
    """
    Creates a child window.
    """

    window = tk.Toplevel(parent)

    window.title(title)

    center_window(
        window,
        width,
        height
    )

    return window