"""
User Login Module

Responsible for authenticating users.

Responsibilities:
- Find user account.
- Verify password.
- Return authenticated user information.

Database operations are handled by:
    database/queries.py
"""


from auth.password_utils import verify_password


from database.queries import (
    get_user_by_username
)



# ==========================================================
# LOGIN USER
# ==========================================================

def login_user(
    username,
    password
):
    """
    Authenticates a user.

    Args:
        username:
            Entered username.

        password:
            Entered plain text password.


    Returns:

        (True, user)

        or

        (False, error message)
    """



    # ======================================================
    # VALIDATION
    # ======================================================

    if username == "":

        return False, (
            "Username is required"
        )



    if password == "":

        return False, (
            "Password is required"
        )



    # ======================================================
    # FIND USER
    # ======================================================

    user = get_user_by_username(
        username
    )



    if user is None:

        return False, (
            "Invalid username or password"
        )



    # ======================================================
    # VERIFY PASSWORD
    # ======================================================

    password_valid = verify_password(
        password,
        user["password"]
    )



    if not password_valid:

        return False, (
            "Invalid username or password"
        )



    # ======================================================
    # LOGIN SUCCESS
    # ======================================================

    return True, user