from flask import Flask, request, send_file, jsonify
from PIL import Image
from flask_cors import CORS
import io
from model import process_image

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Optimized Background Removal API is running!"})

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    try:
        # Check if file is uploaded
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        input_image = Image.open(file)
        
        # Get background color or file
        bg_color = request.args.get("bg", "transparent")
        bg_file = request.files.get("bg_file", None)
        width_str = request.form.get("width")
        height_str = request.form.get("height")

        if not width_str or not height_str:
            return jsonify({"error": "Width and height are required"}), 400

        try:
            width = int(width_str)
            height = int(height_str)
        except ValueError:
            return jsonify({"error": "Width and height must be integers"}), 400


        # Process image (Run in a separate thread for faster response)
        processed_image = process_image(input_image, bg_color, bg_file, output_size=(width, height))

        # Convert image to bytes
        img_bytes = io.BytesIO()
        processed_image.save(img_bytes, format="PNG")
        img_bytes.seek(0)

        return send_file(img_bytes, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Enable multi-threading for handling multiple requests
    app.run(host="0.0.0.0", port=8000, debug=True, threaded=True)
