from fastapi import FastAPI, Request
from conversation import process_message
from sms_provider import send_sms

app = FastAPI()


@app.get("/")
def home():

    return {
        "status": "online",
        "service": "ThittamArivom SMS Bot"
    }


@app.post("/sms/incoming")
async def incoming_sms(request: Request):

    data = await request.json()

    print("Incoming SMS:", data)

    # Routee-style incoming SMS payload
    phone = data.get("from")
    message = data.get("message", "")

    if not phone:
        return {
            "status": "error",
            "message": "Phone number missing"
        }

    reply = process_message(phone, message)

    # Send response
    if reply:
        try:
            send_sms(phone, reply)
        except Exception as e:
            print("SMS sending error:", e)

    return {
        "status": "ok"
    }