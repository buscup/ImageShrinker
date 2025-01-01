from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from SeamCarver import SeamCarver

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return "No file part", 400

        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                remove_columns = int(request.form.get('remove_columns', 0))
                remove_rows = int(request.form.get('remove_rows', 0))
            except ValueError:
                return "Invalid input for rows/columns", 400

            # Process image
            try:
                sc = SeamCarver(filepath)
                for _ in range(remove_rows):
                    seam = sc.find_horizontal_seam()
                    sc.remove_horizontal_seam(seam)

                for _ in range(remove_columns):
                    seam = sc.find_vertical_seam()
                    sc.remove_vertical_seam(seam)

                output_filename = f"processed_{filename}"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                sc.save_image(output_path)

                return redirect(url_for('download', filename=output_filename))
            except Exception as e:
                return f"Error during image processing: {str(e)}", 500
    except Exception as e:
        return f"Unexpected error: {str(e)}", 500

@app.route('/download/<filename>')
def download(filename):
    return render_template('download.html', filename=filename)

@app.route('/files/<filename>')
def files(filename):
    try:
        return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)
    except Exception as e:
        return f"Error serving file: {str(e)}", 500

@app.route('/drag-upload', methods=['POST'])
def drag_upload():
    try:
        if 'file' not in request.files:
            return jsonify(success=False, error="No file part"), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify(success=False, error="No selected file"), 400

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                remove_columns = int(request.form.get('remove_columns', 0) or 0)
                remove_rows = int(request.form.get('remove_rows', 0) or 0)
            except ValueError:
                return jsonify(success=False, error="Invalid input for rows/columns"), 400

            # Process image
            try:
                sc = SeamCarver(filepath)
                for _ in range(remove_rows):
                    seam = sc.find_horizontal_seam()
                    sc.remove_horizontal_seam(seam)

                for _ in range(remove_columns):
                    seam = sc.find_vertical_seam()
                    sc.remove_vertical_seam(seam)

                output_filename = f"processed_{filename}"
                output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
                sc.save_image(output_path)

                return jsonify(success=True, filename=output_filename)
            except Exception as e:
                return jsonify(success=False, error=f"Error during image processing: {str(e)}"), 500
    except Exception as e:
        return jsonify(success=False, error=f"Unexpected error: {str(e)}"), 500

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)

