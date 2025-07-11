from flask import request, jsonify
from . import auth_bp
from .schemas import RequestOTPSchema, VerifyOTPSchema
from .services import request_otp, verify_otp
from app.extensions import logger
from flask_jwt_extended import create_access_token
import logging

@auth_bp.route('/request-otp', methods=['POST'])
def request_otp_route():
    """
    Request OTP for phone number
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - phone
          properties:
            phone:
              type: string
    responses:
      200:
        description: OTP sent successfully
      400:
        description: Validation error
    """
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
    """
    Verify OTP for phone number
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - phone
            - otp
          properties:
            phone:
              type: string
            otp:
              type: string
    responses:
      200:
        description: OTP verified successfully
      400:
        description: Validation error
    """
    data = request.get_json()
    errors = VerifyOTPSchema().validate(data)
    if errors:
        return jsonify({'errors': errors}), 400
    phone = data['phone']
    otp = data['otp']
    result = verify_otp(phone, otp)
    logger.logger.info(f"OTP verification attempted for {phone}")
    if result.get('success'):
        access_token = create_access_token(identity=phone)
        return jsonify({**result, 'access_token': access_token}), 200
    return jsonify(result), 200 