"""
Desktop Chat Server

FastAPI WebSocket backend.

Responsibilities:
- Start FastAPI application.
- Accept WebSocket clients.
- Authenticate client sessions.
- Track online users.
- Broadcast status changes.
- Route messages.
- Save chat messages.
- Handle clean shutdown.
"""


from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect
)


from contextlib import asynccontextmanager

from datetime import datetime

import uvicorn



from websocket_manager import manager


from database.queries import (
    save_message
)





# ==========================================================
# APPLICATION LIFESPAN
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    print(
        "Desktop Chat Server Started"
    )


    yield


    print(
        "Server shutting down..."
    )


    await manager.shutdown()


    print(
        "All connections closed"
    )





# ==========================================================
# CREATE APPLICATION
# ==========================================================

app = FastAPI(

    title="Desktop Chat Server",

    version="1.0",

    lifespan=lifespan

)







# ==========================================================
# ROOT TEST
# ==========================================================

@app.get("/")
def home():

    return {

        "status":
        "Desktop Chat Server Running"

    }








# ==========================================================
# WEBSOCKET ENDPOINT
# ==========================================================

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):


    user_id = None


    await websocket.accept()


    print(
        "New WebSocket connection"
    )



    try:


        while True:


            data = await websocket.receive_json()



            event = data.get(
                "event"
            )



            print(
                "Received:",
                event
            )






            # ==================================================
            # LOGIN
            # ==================================================

            if event == "login":


                login_user_id = data.get(
                    "user_id"
                )



                if not login_user_id:


                    await websocket.send_json(

                        {

                            "event":
                            "error",


                            "message":
                            "Missing user id"

                        }

                    )

                    continue






                user_id = login_user_id





                # Register connection

                await manager.connect(

                    user_id,

                    websocket

                )




                print(

                    f"User {user_id} connected"

                )






                await websocket.send_json(

                    {

                        "event":
                        "login_success",


                        "user_id":
                        user_id

                    }

                )







                await manager.broadcast(

                    {

                        "event":
                        "user_online",


                        "user_id":
                        user_id

                    }

                )









            # ==================================================
            # CHAT MESSAGE
            # ==================================================

            elif event == "message":



                sender_id = data.get(

                    "sender_id"

                )


                receiver_id = data.get(

                    "receiver_id"

                )


                message = data.get(

                    "message"

                )







                # Security check

                if sender_id != user_id:


                    await websocket.send_json(

                        {

                            "event":
                            "error",


                            "message":
                            "Unauthorized sender"

                        }

                    )


                    continue







                if not sender_id or not receiver_id or not message:


                    await websocket.send_json(

                        {

                            "event":
                            "error",


                            "message":
                            "Invalid message data"

                        }

                    )


                    continue







                sent_time = datetime.now().strftime(

                    "%Y-%m-%d %H:%M:%S"

                )







                saved = save_message(

                    sender_id,

                    receiver_id,

                    message,

                    sent_time

                )






                if not saved:


                    await websocket.send_json(

                        {

                            "event":
                            "error",


                            "message":
                            "Could not save message"

                        }

                    )


                    continue







                delivered = await manager.send_private_message(

                    receiver_id,

                    {

                        "event":
                        "message",


                        "sender_id":
                        sender_id,


                        "receiver_id":
                        receiver_id,


                        "message":
                        message,


                        "sent_at":
                        sent_time

                    }

                )








                await websocket.send_json(

                    {

                        "event":
                        "message_sent",


                        "receiver_id":
                        receiver_id,


                        "delivered":
                        delivered

                    }

                )









            # ==================================================
            # LOGOUT
            # ==================================================

            elif event == "logout":



                logout_user = data.get(

                    "user_id"

                )



                if logout_user == user_id:



                    manager.disconnect(

                        logout_user

                    )



                    await manager.broadcast(

                        {

                            "event":
                            "user_offline",


                            "user_id":
                            logout_user

                        }

                    )



                    user_id = None










            # ==================================================
            # HEARTBEAT
            # ==================================================

            elif event == "ping":


                await websocket.send_json(

                    {

                        "event":
                        "pong"

                    }

                )










            # ==================================================
            # UNKNOWN EVENT
            # ==================================================

            else:


                await websocket.send_json(

                    {

                        "event":
                        "error",


                        "message":
                        "Unknown event"

                    }

                )









    except WebSocketDisconnect:


        print(

            "Client disconnected"

        )







    except Exception as error:


        print(

            "Server error:",

            error

        )







    finally:


        if user_id:



            manager.disconnect(

                user_id

            )




            await manager.broadcast(

                {

                    "event":
                    "user_offline",


                    "user_id":
                    user_id

                }

            )




            print(

                f"User {user_id} offline"

            )









# ==========================================================
# START SERVER
# ==========================================================

if __name__ == "__main__":


    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True

    )

    