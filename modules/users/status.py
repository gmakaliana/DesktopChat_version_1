from datetime import datetime

from database.queries import (
    update_user_status,
    update_last_seen
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
    Sets user status to Online.

    Returns:
        True if successful.
        False otherwise.
    """

    status_success = update_user_status(
        user_id,
        "Online"
    )

    last_seen_success = update_last_seen(
        user_id,
        get_current_time()
    )

    return status_success and last_seen_success


# ==========================================================
# SET USER OFFLINE
# ==========================================================

def set_offline(user_id):
    """
    Sets user status to Offline.

    Returns:
        True if successful.
        False otherwise.
    """

    status_success = update_user_status(
        user_id,
        "Offline"
    )

    last_seen_success = update_last_seen(
        user_id,
        get_current_time()
    )

    return status_success and last_seen_success


# ==========================================================
# UPDATE LAST SEEN
# ==========================================================

def update_activity(user_id):
    """
    Updates user's last activity time.

    Returns:
        True if successful.
        False otherwise.
    """

    return update_last_seen(
        user_id,
        get_current_time()
    )