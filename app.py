from flask import Flask, request, jsonify, render_template, send_from_directory, make_response
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
import os
import logging
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['PROCESSED_FOLDER'] = "processed/"
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['PROCESSED_FOLDER']):
    os.makedirs(app.config['PROCESSED_FOLDER'])

SERVER_URL = "http://localhost:5000/upload_files"
logging.basicConfig(level=logging.DEBUG)

processing_status = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/upload_files', methods=['POST', 'OPTIONS'])
def upload_files():
    if request.method == 'OPTIONS':
        return '', 200

    logging.debug("Received request for file upload")
    if 'image' not in request.files or 'video' not in request.files:
        logging.error("No file part in request")
        return jsonify({"error": "No file part"}), 400

    image_file = request.files['image']
    video_file = request.files['video']

    if image_file.filename == '' or video_file.filename == '':
        logging.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    image_filename = secure_filename(image_file.filename)
    video_filename = secure_filename(video_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    image_file.save(image_path)
    video_file.save(video_path)

    request_id = str(uuid.uuid4())
    processing_status[request_id] = 'Processing'

    files = {
        'image': open(image_path, 'rb'),
        'video': open(video_path, 'rb')
    }

    def process_files():
        logging.info(f"Sending request to {SERVER_URL}")
        try:
            response = requests.post(SERVER_URL, files=files)
            response.raise_for_status()
            response_data = response.json()
            logging.info(f"Response from server: {response_data}")

            if response_data['success'] and 'output_video_url' in response_data:
                processed_video_url = response_data['output_video_url']
                processed_video_filename = os.path.basename(processed_video_url)
                processed_video_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_video_filename)

                with requests.get(processed_video_url, stream=True) as r:
                    r.raise_for_status()
                    with open(processed_video_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                response_data['output_video_url'] = f'/processed/{processed_video_filename}'
                processing_status[request_id] = 'Completed'
                processing_status[request_id + '_result'] = response_data
            else:
                processing_status[request_id] = 'Failed'
        except requests.exceptions.RequestException as e:
            logging.error(f"Error connecting to server: {e}")
            processing_status[request_id] = 'Failed'
        finally:
            files['image'].close()
            files['video'].close()

    import threading
    threading.Thread(target=process_files).start()

    return jsonify({"request_id": request_id})

@app.route('/status/<request_id>', methods=['GET'])
def status(request_id):
    status = processing_status.get(request_id, 'Unknown')
    result = processing_status.get(request_id + '_result', None)
    return jsonify({"status": status, "result": result})

@app.route('/processed/<filename>')
def processed_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
