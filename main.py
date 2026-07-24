"""
Application Entry Point

Responsible for starting Desktop Chat System.
"""


from database.create_tables import create_tables
from gui.login_window import open_login_window


from utils.app_paths import (
    get_database_path,
    get_upload_folder,
    get_backup_folder
)



def main():
    """
    Application startup.
    """


    # Create user folders

    get_database_path()

    get_upload_folder()

    get_backup_folder()



    # Create database tables

    create_tables()



    # Start application

    open_login_window()



if __name__ == "__main__":

    main()