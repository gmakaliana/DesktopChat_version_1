"""
WebSocket Connection Manager

Responsible for:

- Tracking connected users.
- Managing WebSocket sessions.
- Sending private messages.
- Broadcasting events.
- Handling disconnects.
- Preventing duplicate connections.
- Handling reconnect replacement.
- Server shutdown cleanup.
"""


from fastapi import WebSocket

from datetime import datetime





# ==========================================================
# CONNECTION MANAGER
# ==========================================================


class ConnectionManager:


    def __init__(self):


        # Stores active connections
        #
        # {
        #     user_id:
        #     {
        #         "socket": websocket,
        #         "connected_at": datetime
        #     }
        # }


        self.active_connections = {}







    # ======================================================
    # CONNECT USER
    # ======================================================

    async def connect(

        self,

        user_id,

        websocket: WebSocket

    ):
        """
        Registers a user connection.

        If user already exists:
        - Close old socket.
        - Replace with new socket.

        Used during reconnect.
        """



        # --------------------------------------------------
        # Remove old connection
        # --------------------------------------------------

        if user_id in self.active_connections:


            old_socket = (

                self.active_connections[user_id]["socket"]

            )


            try:


                await old_socket.close()



            except Exception:


                pass





        # --------------------------------------------------
        # Store new connection
        # --------------------------------------------------


        self.active_connections[user_id] = {


            "socket":

            websocket,


            "connected_at":

            datetime.now()


        }




        print(

            f"User {user_id} connected."

        )









    # ======================================================
    # DISCONNECT USER
    # ======================================================

    def disconnect(

        self,

        user_id,

        websocket=None

    ):
        """
        Removes user connection.

        websocket check prevents
        an old connection from deleting
        a newer reconnect.
        """



        connection = self.active_connections.get(

            user_id

        )



        if not connection:

            return





        # --------------------------------------------------
        # Prevent old socket removing new socket
        # --------------------------------------------------

        if websocket:



            if connection["socket"] != websocket:


                return





        del self.active_connections[user_id]



        print(

            f"User {user_id} disconnected."

        )









    # ======================================================
    # CHECK ONLINE
    # ======================================================

    def is_online(

        self,

        user_id

    ):


        return user_id in self.active_connections









    # ======================================================
    # GET SOCKET
    # ======================================================

    def get_socket(

        self,

        user_id

    ):


        connection = self.active_connections.get(

            user_id

        )


        if connection:


            return connection["socket"]



        return None










    # ======================================================
    # SEND PRIVATE MESSAGE
    # ======================================================

    async def send_private_message(

        self,

        user_id,

        message

    ):
        """
        Sends event to one user.

        Returns:

            True  = delivered
            False = offline
        """



        websocket = self.get_socket(

            user_id

        )



        if not websocket:


            return False






        try:


            await websocket.send_json(

                message

            )


            return True





        except Exception as error:



            print(

                "Private message error:",

                error

            )


            self.disconnect(

                user_id,

                websocket

            )


            return False










    # ======================================================
    # BROADCAST
    # ======================================================

    async def broadcast(

        self,

        message

    ):
        """
        Sends event to every online user.
        """



        disconnected = []




        for user_id, data in list(

            self.active_connections.items()

        ):



            websocket = data["socket"]



            try:


                await websocket.send_json(

                    message

                )



            except Exception as error:



                print(

                    "Broadcast failed:",

                    user_id,

                    error

                )



                disconnected.append(

                    (

                        user_id,

                        websocket

                    )

                )







        # Remove broken sockets

        for user_id, websocket in disconnected:



            self.disconnect(

                user_id,

                websocket

            )









    # ======================================================
    # SHUTDOWN SERVER
    # ======================================================

    async def shutdown(self):
        """
        Closes all active connections.

        Called when FastAPI server stops.
        """



        print(

            "Closing WebSocket connections..."

        )




        for user_id, data in list(

            self.active_connections.items()

        ):



            websocket = data["socket"]



            try:


                await websocket.close()



            except Exception:



                pass






        self.active_connections.clear()





        print(

            "All connections closed."

        )









    # ======================================================
    # ONLINE USERS
    # ======================================================

    def get_online_users(self):


        return list(

            self.active_connections.keys()

        )









    # ======================================================
    # CONNECTION COUNT
    # ======================================================

    def get_connection_count(self):


        return len(

            self.active_connections

        )







# ==========================================================
# SINGLE INSTANCE
# ==========================================================


manager = ConnectionManager()

