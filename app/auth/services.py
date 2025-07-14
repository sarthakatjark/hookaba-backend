import datetime
import random
from app.extensions import mongo
from app.common.sms import send_sms
from app.common.utils import generate_otp
from flask import current_app
import datetime

OTP_COLLECTION = 'otps'

def request_otp(phone):
    otp = generate_otp()
    expiry = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=current_app.config['OTP_EXPIRY_SECONDS'])
    mongo.db[OTP_COLLECTION].update_one(
        {'phone': phone},
        {'$set': {'otp': otp, 'expires_at': expiry}},
        upsert=True
    )
    send_sms(phone, otp)
    return {'message': 'OTP sent'}

def verify_otp(phone, otp):
    record = mongo.db[OTP_COLLECTION].find_one({'phone': phone})
    if not record:
        return {'success': False, 'message': 'OTP not found'}
    if record['otp'] != otp:
        return {'success': False, 'message': 'Invalid OTP'}
    expires_at = record['expires_at']
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=datetime.timezone.utc)
    if datetime.datetime.now(datetime.timezone.utc) > expires_at:
        return {'success': False, 'message': 'OTP expired'}
    # Optionally, delete OTP after successful verification
    mongo.db[OTP_COLLECTION].delete_one({'phone': phone})
    return {'success': True, 'message': 'OTP verified'} 