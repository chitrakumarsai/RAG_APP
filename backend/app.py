import os
from flask import Flask, request
from flask_cors import CORS
from multiprocessing.managers import BaseManager

# Flask app setup
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './data'  # Directory to save uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Connect to the Index Server
manager = BaseManager(("127.0.0.1", 5602), b"password")
manager.register("query_index")
manager.register("insert_into_index")
manager.connect()

@app.route("/", methods=["GET"])
def home():
    return "Hello World!"


@app.route("/query", methods=["GET"])
def query_index():
    """
    Handle GET requests to process user queries.
    """
    query_text = request.args.get("text")
    if not query_text:
        return {"error": "Query text is missing"}, 400

    try:
        # Call the index server to query the index
        response = manager.query_index(query_text)._getvalue()
        return {"answer": response}, 200
    except Exception as e:
        return {"error": str(e)}, 500


@app.route("/uploadFile", methods=["POST"])
def upload_file():
    """
    Handle POST requests to upload files and add them to the index.
    """
    if "file" not in request.files:
        return {"error": "No file provided"}, 400

    # Get the file from the request
    uploaded_file = request.files["file"]
    filename = uploaded_file.filename
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        # Save the file to the upload folder
        uploaded_file.save(filepath)

        # Insert the file into the index via the index server
        manager.insert_into_index(filepath)
        return {"message": "File uploaded and inserted into index!"}, 200
    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5601)
