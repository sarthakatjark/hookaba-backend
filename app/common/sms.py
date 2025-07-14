import os

def send_sms(phone, otp):
    """
    Sends an OTP to the specified phone number using Twilio.
    If SMS_PROVIDER is set to 'mock', prints the OTP to console.
    """
    provider = os.getenv("SMS_PROVIDER", "mock")

    if provider == "twilio":
        from twilio.rest import Client

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")

        if not all([account_sid, auth_token, from_phone]):
            raise ValueError("Twilio configuration missing")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=from_phone,
            to=phone
        )
    else:
        print(f"[MOCK SMS] OTP for {phone}: {otp}") 