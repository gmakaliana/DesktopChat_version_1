"""
Contacts Management Module

Responsible for contact operations.

Responsibilities:
- Search users.
- Add contacts.
- Load user contacts.

GUI should not communicate directly
with database queries.
"""


from database.queries import (
    search_users,
    add_contact,
    get_contacts
)



# ==========================================================
# SEARCH USERS
# ==========================================================

def search_available_users(
    keyword,
    current_user_id
):
    """
    Searches users available to add.

    Searches:

    - Username
    - Full name


    Excludes:

    - Current user


    Returns:
        List of users
    """


    keyword = keyword.strip()



    if not keyword:

        return []



    users = search_users(
        keyword,
        current_user_id
    )


    return users





# ==========================================================
# ADD NEW CONTACT
# ==========================================================

def add_new_contact(
    current_user_id,
    friend_id
):
    """
    Adds a new contact.

    Returns:

        True:
            Contact added

        False:
            Failed or already exists
    """


    success = add_contact(
        current_user_id,
        friend_id
    )



    return success





# ==========================================================
# GET CONTACT LIST
# ==========================================================

def get_user_contacts(
    user_id
):
    """
    Returns user's contacts.

    Used by:
        home_window.py
    """


    contacts = get_contacts(
        user_id
    )


    return contacts





# ==========================================================
# FORMAT USER SEARCH RESULT
# ==========================================================

def format_user_result(
    user
):
    """
    Formats user information
    for displaying in GUI.
    """


    status = user["status"]



    if status == "Online":

        icon = "🟢"


    else:

        icon = "⚪"



    return (

        f"{icon} "

        f"{user['full_name']} "

        f"({user['username']})"

    )