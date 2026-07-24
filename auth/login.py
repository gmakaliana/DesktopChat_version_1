"""
User Login Module

Responsible for authenticating users
in the Desktop Chat System.

This module handles:
- Finding users by username
- Verifying passwords
- Updating user status
- Returning user information

This module does not contain GUI code.
"""


from datetime import datetime

from database.db import get_connection
from auth.password_utils import verify_password



# ==========================================================
# FIND USER BY USERNAME
# ==========================================================

def get_user_by_username(username):
    """
    Retrieves a user from the database using username.

    Args:
        username (str): Username to search.

    Returns:
        sqlite3.Row or None
    """

    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )


    user = cursor.fetchone()


    connection.close()


    return user



# ==========================================================
# UPDATE USER STATUS
# ==========================================================

def update_user_status(user_id, status):
    """
    Updates user's online status.

    Args:
        user_id (int): User ID.
        status (str): Online or Offline.
    """

    connection = get_connection()

    cursor = connection.cursor()


    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    cursor.execute(
        """
        UPDATE users

        SET 
            status = ?,
            last_seen = ?

        WHERE user_id = ?

        """,
        (
            status,
            current_time,
            user_id
        )
    )


    connection.commit()

    connection.close()



# ==========================================================
# LOGIN USER
# ==========================================================

def login_user(username, password):
    """
    Authenticates a user.

    Args:
        username (str): Username.
        password (str): Password entered by user.

    Returns:
        tuple:

        Successful:
            (True, user)

        Failed:
            (False, error message)
    """


    # ------------------------------------------
    # Validate Empty Input
    # ------------------------------------------

    if not username:

        return False, "Username is required."


    if not password:

        return False, "Password is required."



    # ------------------------------------------
    # Find User
    # ------------------------------------------

    user = get_user_by_username(username)



    if user is None:

        return False, "Invalid username or password."



    # ------------------------------------------
    # Verify Password
    # ------------------------------------------

    password_correct = verify_password(
        password,
        user["password"]
    )



    if not password_correct:

        return False, "Invalid username or password."



    # ------------------------------------------
    # Update Status
    # ------------------------------------------

    update_user_status(
        user["user_id"],
        "Online"
    )



    return True, user