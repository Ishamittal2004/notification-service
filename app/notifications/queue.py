import pika, json
# from .email import send_email
# from .sms import send_sms
# from .in_app import send_in_app
from app.notifications.email import send_email
from app.notifications.sms import send_sms
from app.notifications.in_app import send_in_app



def callback(ch, method, properties, body):
    data = json.loads(body)
    type = data["type"]
    message = data["message"]
    try:
        if type == "email":
            send_email(message)
        elif type == "sms":
            send_sms(message)
        elif type == "in_app":
            send_in_app(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Retrying due to:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="notifications")
    channel.basic_consume(queue="notifications", on_message_callback=callback)
    print("📥 Listening for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    consume()

