from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import uuid

app = FastAPI()

# Dictionary to store connected WebSocket clients and their pseudos
connected_users = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/{pseudo}")
async def websocket_endpoint(pseudo: str, websocket: WebSocket):
    await websocket.accept()
    user_id = uuid.uuid4().hex

    # Store the WebSocket connection in the dictionary
    connected_users[user_id] = {"websocket": websocket, "pseudo": pseudo}
    print(connected_users)
    try:
        while True:
            data = await websocket.receive_text()
            print("received " + data)
            # Send the received data to the other users
            for user, user_info in connected_users.items():
                
                await user_info["websocket"].send_text(data)
    except WebSocketDisconnect:
        # If a user disconnects, remove them from the dictionary
        del connected_users[user_id]
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
