from flask import Flask, request, send_file, render_template_string, render_template, send_from_directory
from utils.dmc import dmc_rgb_values
from utils.preprocess_image import create_pattern
from utils.create_pdf import create_pdf
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the file is part of the request
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    
    # Check if the file has a valid filename
    if file.filename == '':
        return "No selected file", 400
    
    if not file or not allowed_file(file.filename):
        return "Invalid file type", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return render_template('pattern_form.html', filename=filename, filepath=filepath) # , filename=filename)

methods_of_dithering = {'none': 1, 'floyd-steinberg': 2, 'atkinson': 3}

@app.route('/pattern', methods=['POST'])
def create_pattern_site():
    filename = request.form['filename']
    width_stitches = int(request.form['width_stitches'])
    number_of_colors = int(request.form['number_of_colors'])
    method_of_dithering = methods_of_dithering[request.form['method_of_dithering']]

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    image = Image.open(image_path)
    width, height = image.size

    if width_stitches > width:
        return "Your pattern can't be bigger than a given image!", 400

    # Creates pattern using data from the form
    pattern = create_pattern(image, width_stitches, number_of_colors, dmc_rgb_values, method_of_dithering)

    name_of_pdf = f"{os.path.splitext(filename)[0]}.pdf"
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], name_of_pdf)
    create_pdf(image, pattern, pdf_path)

    return send_file(pdf_path, as_attachment=True, download_name=pdf_path)

if __name__ == '__main__':
    app.run(debug=False)
