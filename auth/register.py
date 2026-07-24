"""
User Registration Module

Responsible for registering new users
into the Desktop Chat System.

This module handles:
- Username checking
- Password hashing
- Saving user information
- Registration validation

It does not contain GUI code.
"""


from datetime import datetime

from database.db import get_connection
from auth.password_utils import hash_password



# ==========================================================
# CHECK USERNAME EXISTS
# ==========================================================

def username_exists(username):
    """
    Checks whether a username already exists.

    Args:
        username (str): Username to check.

    Returns:
        bool: True if username exists,
              False otherwise.
    """

    connection = get_connection()
    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT user_id
        FROM users
        WHERE username = ?
        """,
        (username,)
    )


    user = cursor.fetchone()


    connection.close()


    return user is not None



# ==========================================================
# REGISTER USER
# ==========================================================

def register_user(username, password, full_name):
    """
    Registers a new user.

    Args:
        username (str): Login username.
        password (str): User password.
        full_name (str): User's full name.

    Returns:
        tuple:
            (True, success message)
            or
            (False, error message)
    """


    # ------------------------------------------
    # Basic Validation
    # ------------------------------------------

    if not username:
        return False, "Username is required."


    if not password:
        return False, "Password is required."


    if not full_name:
        return False, "Full name is required."



    # ------------------------------------------
    # Check Existing Username
    # ------------------------------------------

    if username_exists(username):

        return False, "Username already exists."



    # ------------------------------------------
    # Hash Password
    # ------------------------------------------

    hashed_password = hash_password(password)



    # ------------------------------------------
    # Insert New User
    # ------------------------------------------

    connection = get_connection()
    cursor = connection.cursor()


    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        INSERT INTO users
        (
            username,
            password,
            full_name,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?)

        """,
        (
            username,
            hashed_password,
            full_name,
            "Offline",
            current_time
        )
    )


    connection.commit()

    connection.close()



    return True, "Registration successful."