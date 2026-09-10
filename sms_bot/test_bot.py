from conversation import process_message


phone = "919999999999"

messages = [
    "START",
    "1",
    "25",
    "1",
    "150000",
    "4"
]

for message in messages:

    print("\nUSER:", message)

    reply = process_message(phone, message)

    print("BOT:", reply)