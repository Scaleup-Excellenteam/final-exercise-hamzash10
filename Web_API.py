import os
import time
import uuid

from flask import Flask, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# make the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    handling a POST request to upload a file, and saves the file with a specified UID
    :return: JSON response with the UID of the uploaded file, or an error message if the upload fails.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file found in the request'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    if uploaded_file:
        generated_uid = str(uuid.uuid4())
        timestamp = int(time.time())
        new_filename = f"{uploaded_file.filename[:-5]}_{timestamp}_{generated_uid}.{uploaded_file.filename[-4:]}"
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, new_filename))
        return jsonify({'uid': generated_uid}), 200
    else:
        return jsonify({'error': 'Invalid file'}), 400


if __name__ == '__main__':
    app.run(debug=True)