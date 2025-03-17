from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
import os
from werkzeug.utils import secure_filename
import uuid
from app.ocr_service import process_file
import json

main = Blueprint('main', __name__)


# Remove duplicate function and keep this one
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{original_filename}"

        # Create full path for saving the file
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Create URL-friendly path for template
        display_path = f"/static/uploads/{filename}"

        # Process the image/PDF with OCR
        try:
            text_result, tagged_text = process_file(file_path)

            result = {
                "filename": original_filename,
                "file_path": display_path,
                "text": text_result,
                "tagged_text": tagged_text
            }

            return render_template('results.html', result=result)
        except Exception as e:
            flash(f"Error processing file: {str(e)}")
            return redirect(url_for('main.index'))

    flash("File type not allowed")
    return redirect(url_for('main.index'))


@main.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '')
    text_content = request.form.get('text_content', '')

    if not query or not text_content:
        return jsonify({"error": "Missing query or text content"}), 400

    # Simple case-insensitive search
    text_content_lower = text_content.lower()
    query_lower = query.lower()

    if query_lower in text_content_lower:
        # Find positions for highlighting
        positions = []
        start = 0
        while True:
            start = text_content_lower.find(query_lower, start)
            if start == -1:
                break
            positions.append((start, start + len(query)))
            start += len(query)

        return jsonify({
            "found": True,
            "positions": positions,
            "count": len(positions)
        })

    return jsonify({"found": False})