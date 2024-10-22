from flask import Flask, request, jsonify, send_from_directory
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)  # Enable CORS

# AWS credentials from environment variables
ACCESS_KEY = os.getenv('AKIATQPD7CTYL4VDH2OC')
SECRET_KEY = os.getenv('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')
BUCKET_NAME = 'dee.doss'

# Function to upload to S3
def upload_to_s3(file_name, file_data):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_data)
        return True
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Serve the homepage (index.html)
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

# Serve favicon (optional)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    file_name = file.filename

    # Upload the file to S3
    if upload_to_s3(file_name, file):
        return jsonify({'message': 'Image uploaded successfully'}), 200
    
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
