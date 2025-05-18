# from fastapi import APIRouter
# from .schemas import NotificationCreate, NotificationOut
# from .firebase import db
# import uuid
# import pika, json

# router = APIRouter()

# @router.post("/notifications", response_model=NotificationOut)
# def send_notification(notif: NotificationCreate):
#     notif_id = str(uuid.uuid4())
#     notif_data = notif.dict()
#     notif_data.update({"id": notif_id, "status": "pending"})

#     db.collection("notifications").document(notif_id).set(notif_data)

#     connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
#     channel = connection.channel()
#     channel.queue_declare(queue="notifications")
#     channel.basic_publish(exchange="", routing_key="notifications", body=json.dumps(notif_data))
#     connection.close()

#     return notif_data

# @router.get("/users/{user_id}/notifications", response_model=list[NotificationOut])
# def get_notifications(user_id: int):
#     docs = db.collection("notifications").where("user_id", "==", user_id).stream()
#     return [doc.to_dict() for doc in docs]
from fastapi import APIRouter, HTTPException
from app.schemas import NotificationRequest
from app.notifications import email, sms, in_app

router = APIRouter()

# In-memory storage for notifications
user_notifications = {}

@router.post("/notifications")
def send_notification(payload: NotificationRequest):
    if payload.type == "email":
        email.send(payload.user_id, payload.message)
    elif payload.type == "sms":
        sms.send(payload.user_id, payload.message)
    elif payload.type == "in_app":
        in_app.send(payload.user_id, payload.message)
    else:
        raise HTTPException(status_code=400, detail="Invalid notification type")

    user_notifications.setdefault(payload.user_id, []).append(payload.message)
    return {"status": "sent", "type": payload.type}


@router.get("/users/{user_id}/notifications")
def get_user_notifications(user_id: str):
    return user_notifications.get(user_id, [])
