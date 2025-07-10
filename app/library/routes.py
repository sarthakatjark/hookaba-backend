import os
import boto3
from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import library_bp
from .services import add_library_item
from .schemas import LibraryItemSchema

# S3 config (set these in your environment or config)
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")

s3 = boto3.client("s3")

@library_bp.route('/library/upload', methods=['POST'])
def upload_file():
    """
    Upload an image or gif to S3 and store its URL, user ID, and upload time in MongoDB
    ---
    tags:
      - Library
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: file
        type: file
        required: true
      - in: formData
        name: user_id
        type: string
        required: true
    responses:
      201:
        description: File uploaded and stored
      400:
        description: No file, invalid file, or missing user_id
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    user_id = request.form.get('user_id')
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    filename = secure_filename(file.filename)
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        filename,
        ExtraArgs={'ContentType': file.content_type}
    )
    file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
    item_id = add_library_item(file_url, user_id)
    return jsonify({"message": "File uploaded", "id": item_id, "url": file_url}), 201 