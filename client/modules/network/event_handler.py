"""
WebSocket Event Handler

Responsible for processing events received
from the Desktop Chat Server.

Responsibilities:
- Decode server JSON events.
- Dispatch events to multiple callbacks.
- Manage event listeners.
- Support dynamic GUI event registration.
"""



import json






# ==========================================================
# EVENT CALLBACK STORAGE
# ==========================================================

# Format:
#
# {
#     "message": [
#           callback1,
#           callback2
#     ]
# }

callbacks = {}








# ==========================================================
# REGISTER EVENT CALLBACK
# ==========================================================

def register_event(
    event_name,
    callback
):
    """
    Registers a callback for an event.

    Multiple listeners are supported.

    Example:

        register_event(
            "message",
            chat_handler
        )
    """


    if event_name not in callbacks:

        callbacks[event_name] = []




    if callback not in callbacks[event_name]:


        callbacks[event_name].append(

            callback

        )









# ==========================================================
# REMOVE EVENT CALLBACK
# ==========================================================

def remove_event(
    event_name,
    callback=None
):
    """
    Removes callback.

    callback=None removes all listeners
    for that event.
    """


    if event_name not in callbacks:

        return





    # Remove all callbacks

    if callback is None:


        del callbacks[event_name]


        return






    # Remove specific callback

    if callback in callbacks[event_name]:


        callbacks[event_name].remove(

            callback

        )





    if not callbacks[event_name]:


        del callbacks[event_name]









# ==========================================================
# CLEAR ALL EVENTS
# ==========================================================

def clear_events():
    """
    Removes all registered callbacks.
    """

    callbacks.clear()










# ==========================================================
# HANDLE SERVER EVENT
# ==========================================================

def handle_event(
    data
):
    """
    Receives event from websocket client.

    Accepts:

    - JSON string
    - Dictionary
    """



    try:



        # Convert JSON

        if isinstance(data, str):


            data = json.loads(

                data

            )







        event = data.get(

            "event"

        )




        if not event:


            print(

                "Invalid event:",

                data

            )


            return







        listeners = callbacks.get(

            event,

            []

        )






        if not listeners:


            print(

                "No listener for:",

                event

            )


            return







        # Execute all listeners

        for callback in list(listeners):


            try:


                callback(

                    data

                )


            except Exception as error:


                print(

                    "Event callback error:",

                    error

                )






    except Exception as error:


        print(

            "Event handler error:",

            error

        )









# ==========================================================
# DEBUG INFORMATION
# ==========================================================

def get_registered_events():
    """
    Returns registered event names.
    """

    return list(

        callbacks.keys()

    )

