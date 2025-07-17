import os
import boto3
from flask import request, jsonify
from werkzeug.utils import secure_filename
from . import library_bp
from .services import add_library_item
from .schemas import LibraryItemSchema
from flask_jwt_extended import jwt_required
import logging
import imageio
from PIL import Image
import io

# S3 config (set these in your environment or config)
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")

s3 = boto3.client("s3")

def compress_gif(file_stream, max_size=(64, 64), colors=256, frame_skip=2):
    try:
        reader = imageio.get_reader(file_stream, format='gif')
        meta = reader.get_meta_data()
        frames = []
        durations = []
        for i, frame in enumerate(reader):
            if i % frame_skip != 0:
                continue  # Skip frames to reduce total frame count
            im = Image.fromarray(frame)
              # Convert to RGB for better quantization
            im = im.resize(max_size, Image.Resampling.LANCZOS)
            # Quantize to reduce colors, but keep more than 64 for better quality
            im = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
            frames.append(im)
            # Use per-frame duration if available, else fallback to meta
            if isinstance(meta.get('duration'), list):
                durations.append(meta['duration'][i])
            else:
                durations.append(meta.get('duration', 100))
        output = io.BytesIO()
        frames[0].save(
            output,
            format='GIF',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            loop=0,
            duration=durations
        )
        output.seek(0)
        return output
    except Exception as e:
        logging.exception("Failed to compress GIF")
        return None

def compress_image(file_stream, max_size=(64, 64), quality=85):
    try:
        im = Image.open(file_stream)
        im = im.convert('RGB')  # Ensure JPEG compatibility
        im = im.resize(max_size, Image.Resampling.LANCZOS)
        output = io.BytesIO()
        im.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        return output
    except Exception as e:
        logging.exception("Failed to compress image")
        return None

@library_bp.route('/library/upload', methods=['POST'])
@jwt_required()
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
      500:
        description: Internal server error
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({"error": "Missing user_id"}), 400
        file_type = request.form.get('type')
        if not file_type:
            # Infer type from MIME or extension
            if file.content_type.startswith('image/'):
                if file.content_type == 'image/gif' or file.filename.lower().endswith('.gif'):
                    file_type = 'gif'
                else:
                    file_type = 'image'
            else:
                # Add more inference rules as needed
                file_type = None
        if not file_type:
            return jsonify({"error": "Missing or undetectable type"}), 400
        category = request.form.get('category')
        if not category:
            return jsonify({"error": "Missing category"}), 400
        filename = secure_filename(file.filename)
        # --- GIF/image compression logic ---
        if file_type == 'gif':
            compressed = compress_gif(file.stream)
            if compressed is None:
                return jsonify({"error": "GIF compression failed"}), 500
            upload_stream = compressed
        elif file_type == 'image':
            compressed = compress_image(file.stream)
            if compressed is None:
                return jsonify({"error": "Image compression failed"}), 500
            upload_stream = compressed
        else:
            upload_stream = file.stream
        try:
            s3.upload_fileobj(
                upload_stream,
                S3_BUCKET,
                filename,
                ExtraArgs={'ContentType': file.content_type}
            )
        except Exception as e:
            logging.exception("S3 upload failed")
            return jsonify({"error": "Failed to upload file to S3", "details": str(e)}), 500
        file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{filename}"
        try:
            item_id = add_library_item(file_url, user_id, file_type, category)
        except Exception as e:
            logging.exception("Failed to save library item to DB")
            return jsonify({"error": "Failed to save library item", "details": str(e)}), 500
        return jsonify({"message": "File uploaded", "id": item_id, "url": file_url, "type": file_type, "category": category}), 201
    except Exception as e:
        logging.exception("Unexpected error in upload_file")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@library_bp.route('/library', methods=['GET'])
@jwt_required()
def list_library_items():
    """
    List all library items with pagination
    ---
    tags:
      - Library
    parameters:
      - in: query
        name: page
        type: integer
        required: false
        default: 1
      - in: query
        name: per_page
        type: integer
        required: false
        default: 10
    responses:
      200:
        description: Paginated list of library items
      500:
        description: Internal server error
    """
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        from .services import get_library_items
        try:
            items, total, total_pages = get_library_items(page, per_page)
        except Exception as e:
            logging.exception("Failed to fetch library items from DB")
            return jsonify({"error": "Failed to fetch library items", "details": str(e)}), 500
        schema = LibraryItemSchema(many=True)
        return jsonify({
            "items": schema.dump(items),
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages
        }), 200
    except Exception as e:
        logging.exception("Unexpected error in list_library_items")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500 