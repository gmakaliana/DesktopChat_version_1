"""
User Management Module

Responsible for user-related business logic.

Responsibilities:
- Retrieve user profiles.
- Update user information.
- Manage user status.
- Search users.

Database operations are handled by:
    database/queries.py
"""


from database.queries import (
    get_user_by_id,
    search_users,
    update_user_status,
    update_last_seen
)



# ==========================================================
# GET USER PROFILE
# ==========================================================

def get_profile(user_id):
    """
    Retrieves a user's profile information.

    Args:
        user_id:
            ID of the user.

    Returns:
        User record or None
    """


    user = get_user_by_id(
        user_id
    )


    return user



# ==========================================================
# SEARCH USERS
# ==========================================================

def find_users(keyword):
    """
    Searches for users.

    Used when adding contacts.

    Args:
        keyword:
            Username or full name.

    Returns:
        List of users.
    """


    users = search_users(
        keyword
    )


    return users



# ==========================================================
# SET USER ONLINE
# ==========================================================

def set_online(user_id):
    """
    Changes user status to Online.
    """


    update_user_status(
        user_id,
        "Online"
    )



# ==========================================================
# SET USER OFFLINE
# ==========================================================

def set_offline(
    user_id,
    last_seen
):
    """
    Changes user status to Offline
    and updates last seen time.

    Args:
        user_id:
            User identifier.

        last_seen:
            Current date and time.
    """


    update_user_status(
        user_id,
        "Offline"
    )


    update_last_seen(
        user_id,
        last_seen
    )



# ==========================================================
# UPDATE USERNAME
# ==========================================================

def update_username(
    user_id,
    new_username
):
    """
    Placeholder for username update.

    This requires an additional database
    query function.

    Future implementation:
        database/queries.py
        update_username()
    """


    return False, (
        "Username update not implemented yet"
    )



# ==========================================================
# UPDATE PROFILE PICTURE
# ==========================================================

def update_profile_picture(
    user_id,
    picture_path
):
    """
    Placeholder for profile picture update.

    The database query will be added later.

    Future:
        users.profile_picture
    """


    return False, (
        "Profile picture update not implemented yet"
    )