"""
Application Path Manager

Responsible for managing all user data locations.

The application files remain inside the program folder.

User-generated data is stored separately:

Documents/
    Desktop Chat/
        database/
        uploads/
        backups/

This structure supports PyInstaller deployment.
"""


from pathlib import Path
import os



# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

APP_NAME = "Desktop Chat"



# ==========================================================
# DOCUMENTS FOLDER
# ==========================================================

def get_documents_folder():
    """
    Returns the user's Documents folder.
    """

    return Path.home() / "Documents"



# ==========================================================
# APPLICATION DATA FOLDER
# ==========================================================

def get_app_data_folder():
    """
    Returns Desktop Chat user data folder.
    """

    folder = (
        get_documents_folder()
        /
        APP_NAME
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



# ==========================================================
# DATABASE PATH
# ==========================================================

def get_database_folder():
    """
    Returns database storage folder.
    """

    folder = (
        get_app_data_folder()
        /
        "database"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_database_path():
    """
    Returns SQLite database file path.
    """

    return (
        get_database_folder()
        /
        "chat.db"
    )



# ==========================================================
# UPLOAD PATHS
# ==========================================================

def get_upload_folder():

    folder = (
        get_app_data_folder()
        /
        "uploads"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_profile_folder():

    folder = (
        get_upload_folder()
        /
        "profiles"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_image_folder():

    folder = (
        get_upload_folder()
        /
        "images"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



# ==========================================================
# BACKUP PATH
# ==========================================================

def get_backup_folder():

    folder = (
        get_app_data_folder()
        /
        "backup"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder