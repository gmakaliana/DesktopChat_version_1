"""
Password Utility Module

Responsible for securely hashing passwords and
verifying user passwords using the bcrypt algorithm.

Passwords are never stored in plain text.
"""

import bcrypt


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password):
    """
    Hashes a plain-text password.

    Args:
        password (str): User password.

    Returns:
        str: Hashed password.
    """

    # Convert password into bytes
    password_bytes = password.encode("utf-8")

    # Generate password hash
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    # Convert bytes back to string before storing
    return hashed_password.decode("utf-8")


# ==========================================================
# VERIFY PASSWORD
# ==========================================================

def verify_password(password, hashed_password):
    """
    Verifies whether a password matches its stored hash.

    Args:
        password (str): Password entered by the user.
        hashed_password (str): Password hash stored in the database.

    Returns:
        bool: True if the password is correct, otherwise False.
    """

    # Convert both values into bytes
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    # Compare password with stored hash
    return bcrypt.checkpw(
        password_bytes,
        hashed_password_bytes
    )