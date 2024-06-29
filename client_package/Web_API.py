import os
import time
import uuid
from Modules import UPLOAD_FOLDER, OUTPUT_FOLDER
from flask import Flask, request, jsonify
import logging
from logging.handlers import TimedRotatingFileHandler

app = Flask(__name__)


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FLASK_LOG_DIR = os.path.join(parent_dir, 'logs', 'flask_server')

# Create the logging directory if it doesn't exist
if not os.path.exists(FLASK_LOG_DIR):
    os.makedirs(FLASK_LOG_DIR)

# Configure TimedRotatingFileHandler for daily log rotation
log_file = os.path.join(FLASK_LOG_DIR, 'web_api.log')
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)

# Add the handler to the Flask's default logger
if not app.logger.hasHandlers():
    app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

# Additionally, add the handler to the root logger
root_logger = logging.getLogger()
if not root_logger.hasHandlers():
    root_logger.addHandler(handler)
root_logger.setLevel(logging.DEBUG)


# make the uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# make the outputs directory if it doesn't exist
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    handling a POST request to upload a file, and saves the file with a specified UID
    :return: JSON response with the UID of the uploaded file, or an error message if the upload fails.
    """
    if 'file' not in request.files:
        #app.logger.error('No file found in the request')
        return jsonify({'error': 'No file found in the request'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        #app.logger.error('No file selected for uploading')
        return jsonify({'error': 'No file selected for uploading'}), 400

    if uploaded_file:
        generated_uid = str(uuid.uuid4())
        timestamp = int(time.time())
        new_filename = f"{uploaded_file.filename[:-5]}_{timestamp}_{generated_uid}.{uploaded_file.filename[-4:]}"
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, new_filename))
        #app.logger.info(f"file uploaded successfully with UID {generated_uid}")
        return jsonify({'uid': generated_uid}), 200
    else:
        #app.logger.error("invalid file")
        return jsonify({'error': 'Invalid file'}), 400


@app.route('/status', methods=['GET'])
def status():
    """
    Handling a GET request to get a file explanation using a UID
    :return: JSON response with the all the details required
    """
    received_uid = request.args.get('uid')
    if not received_uid:
        # bad request
        #app.logger.error('No received UID')
        return jsonify({'error': 'No received UID'}), 400

    # check the outputs folder
    for full_filename in os.listdir(OUTPUT_FOLDER):
        if received_uid in full_filename:
            with open(os.path.join(OUTPUT_FOLDER, full_filename), 'r') as f:
                explanation = f.read()

            filename, timestamp, uid_and_extension = full_filename.split('_')

            #app.logger.info(f"file processed successfully")
            # ok
            return jsonify({
                'status': 'done',
                'filename': filename,
                'timestamp': timestamp,
                'explanation': explanation
            }), 200

    # check the uploads folder
    for full_filename in os.listdir(UPLOAD_FOLDER):
        if received_uid in full_filename:
            filename, timestamp, uid_and_extension = full_filename.split('_')
            #app.logger.info("the file explanation is pending")
            # Accepted ( the file exist but hasn't been processed yet )
            return jsonify({
                'status': 'pending',
                'filename': filename,
                'timestamp': timestamp,
                'explanation': ''
            }), 202

    #app.logger.error("the file does not exist")
    # Not Found
    return jsonify({
        'status': 'not found',
        'filename': '',
        'timestamp': '',
        'explanation': ''
    }), 404


if __name__ == '__main__':
    app.run(debug=True)
