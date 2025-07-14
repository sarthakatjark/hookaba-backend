import os

def send_sms(phone, otp, platform=None):
    """
    Sends an OTP to the specified phone number using Twilio.
    If SMS_PROVIDER is set to 'mock', prints the OTP to console.
    The message format is compatible with Android and iOS auto-fill.
    """
    provider = os.getenv("SMS_PROVIDER", "mock")

    if platform == 'ios':
        message_body = f"{otp} is your Hookaba verification code."
    else:  # Default to Android format
        message_body = f"<#> Your Hookaba code is: {otp}\nFA+9qCX9VSu"

    if provider == "twilio":
        from twilio.rest import Client

        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")

        if not all([account_sid, auth_token, from_phone]):
            raise ValueError("Twilio configuration missing")

        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=message_body,
            from_=from_phone,
            to=phone
        )
    else:
        print(f"[MOCK SMS] {message_body}") 