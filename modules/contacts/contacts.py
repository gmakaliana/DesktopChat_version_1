"""
Contact Management Module

Responsible for managing user contacts.

Responsibilities:
- Add contacts.
- Remove contacts.
- Retrieve contacts.
- Search users.

Database operations are handled by:
    database/queries.py
"""


from database.queries import (
    add_contact,
    get_contacts,
    search_users
)



# ==========================================================
# SEARCH AVAILABLE USERS
# ==========================================================

def search_available_users(keyword):
    """
    Searches registered users.

    Used when a user wants to
    find someone to add.

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
# ADD CONTACT
# ==========================================================

def add_new_contact(
    user_id,
    friend_id
):
    """
    Adds another user as a contact.

    Args:
        user_id:
            Current logged-in user.

        friend_id:
            User being added.

    Returns:
        Success status and message.
    """



    # ------------------------------------------------------
    # Prevent adding yourself
    # ------------------------------------------------------

    if user_id == friend_id:

        return False, (
            "You cannot add yourself "
            "as a contact"
        )



    try:


        add_contact(
            user_id,
            friend_id
        )


        return True, (
            "Contact added successfully"
        )



    except Exception:


        return False, (
            "Unable to add contact"
        )



# ==========================================================
# GET USER CONTACTS
# ==========================================================

def get_user_contacts(user_id):
    """
    Returns contacts belonging to a user.

    Converts sqlite rows into
    dictionary objects for GUI use.
    """


    rows = get_contacts(user_id)


    contacts = []


    for row in rows:

        contacts.append(
            {
                "user_id": row["user_id"],
                "username": row["username"],
                "full_name": row["full_name"],
                "profile_picture": row["profile_picture"]
            }
        )


    return contacts



# ==========================================================
# REMOVE CONTACT
# ==========================================================

def remove_contact(
    user_id,
    friend_id
):
    """
    Removes a contact.

    Currently requires a database
    delete query.

    Future implementation:

        database/queries.py
        delete_contact()

    """


    return False, (
        "Remove contact not implemented yet"
    )