"""
User Registration Module

Responsible for creating new user accounts.

Responsibilities:
- Validate registration information.
- Hash passwords.
- Create users through database layer.

Database operations are handled by:
    database/queries.py
"""


from datetime import datetime


from auth.password_utils import hash_password


from database.queries import create_user



# ==========================================================
# REGISTER USER
# ==========================================================

def register_user(
    username,
    password,
    full_name
):
    """
    Creates a new user account.

    Args:
        username:
            New username.

        password:
            Plain text password.

        full_name:
            User's full name.


    Returns:
        tuple:
            (True, message)
            (False, error message)
    """



    # ======================================================
    # BASIC VALIDATION
    # ======================================================

    if username == "":

        return False, "Username is required"



    if password == "":

        return False, "Password is required"



    if full_name == "":

        return False, "Full name is required"



    # ======================================================
    # PASSWORD LENGTH CHECK
    # ======================================================

    if len(password) < 8:

        return False, (
            "Password must contain "
            "at least 8 characters"
        )



    # ======================================================
    # HASH PASSWORD
    # ======================================================

    hashed_password = hash_password(
        password
    )



    # ======================================================
    # CREATE USER
    # ======================================================

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



    success = create_user(
        username,
        hashed_password,
        full_name,
        created_at
    )



    if success:

        return True, (
            "Account created successfully"
        )



    else:

        return False, (
            "Username already exists"
        )