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

Supports:
- Normal Python execution
- PyInstaller deployment
- Moving application between computers
"""


from pathlib import Path



# ==========================================================
# APPLICATION INFORMATION
# ==========================================================

APP_NAME = "Desktop Chat"



# ==========================================================
# DOCUMENTS FOLDER
# ==========================================================

def get_documents_folder():
    """
    Returns user's Documents folder.
    """

    return Path.home() / "Documents"



# ==========================================================
# APPLICATION DATA FOLDER
# ==========================================================

def get_app_data_folder():
    """
    Main application data folder.
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



def get_document_folder():

    folder = (
        get_upload_folder()
        /
        "documents"
    )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    return folder



def get_other_folder():

    folder = (
        get_upload_folder()
        /
        "others"
    )


    folder.mkdir(
        parents=True,
        exist_ok=True
    )


    return folder



# ==========================================================
# RELATIVE FILE PATH SUPPORT
# ==========================================================

def get_relative_file_path(full_path):
    """
    Converts absolute path into database-safe relative path.

    Example:

    Input:

    C:/Users/George/Documents/Desktop Chat/uploads/images/photo.jpg


    Output:

    uploads/images/photo.jpg
    """


    app_folder = get_app_data_folder()


    relative_path = Path(full_path).relative_to(
        app_folder
    )


    return str(relative_path)



def get_absolute_file_path(relative_path):
    """
    Converts database relative path back
    into a real computer path.

    Example:

    Database:

    uploads/images/photo.jpg


    Returns:

    C:/Users/John/Documents/Desktop Chat/uploads/images/photo.jpg
    """


    return (
        get_app_data_folder()
        /
        relative_path
    )



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

# ==========================================================
# DOWNLOAD PATHS
# ==========================================================

def get_download_folder():

    folder = (
        get_app_data_folder()
        /
        "downloads"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_download_image_folder():

    folder = (
        get_download_folder()
        /
        "images"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder


def get_download_document_folder():

    folder = (
        get_download_folder()
        /
        "documents"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder



def get_download_other_folder():

    folder = (
        get_download_folder()
        /
        "others"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    return folder

