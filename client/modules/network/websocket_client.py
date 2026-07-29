"""
WebSocket Client

Handles communication with FastAPI server.

Responsibilities:
- Connect to server.
- Send JSON events.
- Receive events.
- Maintain heartbeat.
- Automatically reconnect.
- Restore login session.
- Forward events to event handler.
"""


import json
import threading
import time
import websocket


from modules.network.event_handler import handle_event





SERVER_URL = "ws://127.0.0.1:8000/ws"







# ==========================================================
# CLIENT
# ==========================================================


class WebSocketClient:


    def __init__(self):


        self.ws = None


        self.connected = False


        self.running = False


        self.user_id = None


        self.callback = None


        self.reconnecting = False


        self.reconnect_attempts = 0







    # ======================================================
    # CONNECT
    # ======================================================

    def connect(self):


        if self.connected:

            return True




        try:


            self.ws = websocket.WebSocket()


            self.ws.connect(

                SERVER_URL

            )



            self.connected = True


            self.running = True


            self.reconnect_attempts = 0



            print(

                "Connected to server."

            )





            threading.Thread(

                target=self.receive_loop,

                daemon=True

            ).start()




            threading.Thread(

                target=self.heartbeat_loop,

                daemon=True

            ).start()



            return True






        except Exception as error:


            print(

                "Connection failed:",

                error

            )



            self.connected = False


            self.ws = None



            return False







    # ======================================================
    # SEND
    # ======================================================

    def send(

        self,

        data

    ):


        if not self.connected or not self.ws:


            return False





        try:


            self.ws.send(

                json.dumps(data)

            )


            return True





        except Exception as error:


            print(

                "Send error:",

                error

            )


            self.connected = False


            return False







    # ======================================================
    # RECEIVE LOOP
    # ======================================================

    def receive_loop(self):


        while self.running:


            try:


                message = self.ws.recv()



                if message:


                    # Main event dispatcher

                    handle_event(

                        message

                    )




                    # Legacy callback only

                    if self.callback:


                        self.callback(

                            json.loads(message)

                        )







            except Exception as error:



                print(

                    "Connection lost:",

                    error

                )



                self.connected = False



                if self.running:

                    self.reconnect()



                break







    # ======================================================
    # HEARTBEAT
    # ======================================================

    def heartbeat_loop(self):


        while self.running:


            time.sleep(30)



            if not self.running:

                break





            if self.connected:


                success = self.send(

                    {

                        "event":

                        "ping"

                    }

                )



                if success:


                    print(

                        "Heartbeat sent."

                    )









    # ======================================================
    # RECONNECT
    # ======================================================

    def reconnect(self):


        if self.reconnecting:

            return



        self.reconnecting = True




        try:



            while not self.connected and self.running:


                self.reconnect_attempts += 1



                print(

                    f"Reconnect attempt {self.reconnect_attempts}"

                )



                time.sleep(5)




                if self.connect():



                    print(

                        "Reconnected successfully."

                    )




                    # Restore session


                    if self.user_id:



                        self.send(

                            {

                                "event":

                                "login",


                                "user_id":

                                self.user_id

                            }

                        )



                    break





        finally:


            self.reconnecting = False







    # ======================================================
    # SAVE USER SESSION
    # ======================================================

    def set_user(

        self,

        user_id

    ):


        self.user_id = user_id







    # ======================================================
    # CALLBACK
    # ======================================================

    def set_callback(

        self,

        callback

    ):


        self.callback = callback







    # ======================================================
    # DISCONNECT
    # ======================================================

    def disconnect(self):


        self.running = False


        self.connected = False



        if self.ws:


            try:


                self.ws.close()



            except Exception:


                pass





        self.ws = None



        print(

            "Disconnected from server."

        )









# ==========================================================
# SINGLE INSTANCE
# ==========================================================


client = WebSocketClient()

