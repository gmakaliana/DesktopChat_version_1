"""
User Status Module

Responsible for managing user presence information.

Features:
- Set user online status
- Set user offline status
- Update last seen time
- Retrieve user status

Database operations are handled through:
    database/queries.py
"""


from datetime import datetime


from database.queries import (
    update_user_status,
    update_last_seen,
    get_user_by_id
)



# ==========================================================
# GET CURRENT TIME
# ==========================================================

def get_current_time():
    """
    Returns current date and time.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



# ==========================================================
# SET USER ONLINE
# ==========================================================

def set_online(user_id):
    """
    Changes user status to Online.

    Args:
        user_id:
            Logged-in user ID.
    """


    update_user_status(
        user_id,
        "Online"
    )


    return True



# ==========================================================
# SET USER OFFLINE
# ==========================================================

def set_offline(user_id):
    """
    Changes user status to Offline
    and updates last seen time.
    """


    update_user_status(
        user_id,
        "Offline"
    )


    update_last_seen(
        user_id,
        get_current_time()
    )


    return True



# ==========================================================
# UPDATE LAST SEEN
# ==========================================================

def update_user_last_seen(user_id):
    """
    Updates only last seen time.
    """


    update_last_seen(
        user_id,
        get_current_time()
    )


    return True



# ==========================================================
# GET USER STATUS
# ==========================================================

def get_status(user_id):
    """
    Returns current user status.

    Example:

    {
        "status": "Online",
        "last_seen": "2026-07-24 23:30:00"
    }
    """


    user = get_user_by_id(
        user_id
    )


    if user:


        return {

            "status": user["status"],

            "last_seen": user["last_seen"]

        }


    return None