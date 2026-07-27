"""
Contacts Management Module

Responsible for contact operations.

Responsibilities:
- Search users.
- Add contacts.
- Remove contacts.
- Load user contacts.
- Format contact display data.

GUI should not communicate directly
with database queries.
"""


from database.queries import (

    search_users,

    add_contact,

    remove_contact,

    get_contacts,

    contact_exists,

    get_contact_count

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
    - Existing contacts


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

    Protection:

    - Cannot add yourself
    - Cannot add duplicate contact


    Returns:

        True:
            Contact added

        False:
            Failed
    """



    if current_user_id == friend_id:

        return False



    if contact_exists(
        current_user_id,
        friend_id
    ):

        return False



    success = add_contact(
        current_user_id,
        friend_id
    )



    return success





# ==========================================================
# REMOVE CONTACT
# ==========================================================

def remove_existing_contact(
    current_user_id,
    friend_id
):
    """
    Removes contact relationship.

    Removes both directions:

        User -> Friend

        Friend -> User


    Returns:

        True:
            Removed

        False:
            Failed
    """



    return remove_contact(
        current_user_id,
        friend_id
    )





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
        contacts_window.py
    """


    contacts = get_contacts(
        user_id
    )


    return contacts





# ==========================================================
# GET CONTACT COUNT
# ==========================================================

def get_user_contact_count(
    user_id
):
    """
    Returns number of contacts.

    Used for:

        - Contact statistics
        - UI counters
    """


    return get_contact_count(
        user_id
    )





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



    if user["status"] == "Online":

        icon = "🟢"


    else:

        icon = "⚪"



    return (

        f"{icon} "

        f"{user['full_name']} "

        f"({user['username']})"

    )





# ==========================================================
# FORMAT CONTACT DISPLAY
# ==========================================================

def format_contact_display(
    contact
):
    """
    Formats contact list display.

    Shows:

    - Status
    - Name
    - Username
    - Last seen
    """



    if contact["status"] == "Online":

        icon = "🟢"


        return (

            f"{icon} "

            f"{contact['full_name']} "

            f"({contact['username']})"

        )



    else:

        icon = "⚪"



        return (

            f"{icon} "

            f"{contact['full_name']} "

            f"({contact['username']}) "

            f"- Last seen: "

            f"{contact['last_seen']}"

        )