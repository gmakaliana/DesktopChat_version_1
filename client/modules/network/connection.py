"""
Connection Helper

Provides communication between
Tkinter application and WebSocket client.

Responsibilities:
- Connect to server.
- Disconnect from server.
- Send events.
- Register event handlers.
- Remove event handlers.
- Check connection status.
- Manage logged-in user session.
"""





from modules.network.websocket_client import (
    client
)



from modules.network.event_handler import (
    register_event,
    remove_event
)









# ==========================================================
# CONNECT
# ==========================================================

def connect_to_server():
    """
    Connects application to WebSocket server.

    Returns:

        True  - connected
        False - failed
    """


    return client.connect()









# ==========================================================
# DISCONNECT
# ==========================================================

def disconnect_from_server():
    """
    Disconnects WebSocket client.
    """


    client.disconnect()









# ==========================================================
# SEND EVENT
# ==========================================================

def send_event(
    data
):
    """
    Sends event to server.
    """


    return client.send(

        data

    )









# ==========================================================
# LEGACY SEND WRAPPER
# ==========================================================

def send_to_server(
    data
):
    """
    Backward compatibility.
    """


    return send_event(

        data

    )









# ==========================================================
# USER SESSION
# ==========================================================

def set_current_user(
    user_id
):
    """
    Stores logged-in user.

    Used for automatic reconnect.
    """


    client.set_user(

        user_id

    )









# ==========================================================
# EVENT REGISTRATION
# ==========================================================

def register_server_event(

    event_name,

    callback

):
    """
    Registers server event listener.
    """


    register_event(

        event_name,

        callback

    )









# ==========================================================
# REMOVE EVENT
# ==========================================================

def unregister_server_event(

    event_name,

    callback=None

):
    """
    Removes event listener.
    """


    remove_event(

        event_name,

        callback

    )









# ==========================================================
# CONNECTION STATUS
# ==========================================================

def is_connected():
    """
    Returns current connection status.
    """


    return client.connected









# ==========================================================
# RECONNECT STATUS
# ==========================================================

def is_reconnecting():
    """
    Checks if reconnect process is running.
    """


    return client.reconnecting









# ==========================================================
# CURRENT USER
# ==========================================================

def get_current_user():
    """
    Returns logged-in user id.
    """


    return client.user_id

