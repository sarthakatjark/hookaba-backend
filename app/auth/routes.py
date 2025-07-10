from flask import request, jsonify
from . import auth_bp
from .schemas import RequestOTPSchema, VerifyOTPSchema
from .services import request_otp, verify_otp
from app.extensions import logger

@auth_bp.route('/request-otp', methods=['POST'])
def request_otp_route():
    data = request.get_json()
    errors = RequestOTPSchema().validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    phone = data['phone']
    result = request_otp(phone)
    logger.logger.info(f"OTP requested for {phone}")
    return jsonify(result), 200

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.get_json()
    errors = VerifyOTPSchema().validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    phone = data['phone']
    otp = data['otp']
    result = verify_otp(phone, otp)
    logger.logger.info(f"OTP verification attempted for {phone}")
    return jsonify(result), 200 