import os
import logging
from flask import Flask, request, render_template
from flask_cors import CORS
from resumeParser.pdf_reader import extract_text_from_pdf, extract_text_from_docx
from resumeParser.parser import parse_resume
from resumeParser.utils import clean_text

# Configure logging for better debugging and info tracking
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

CORS(app)

UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf', '.docx'}

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has an allowed extension."""
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    """Render the homepage with upload form."""
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    """Handle resume upload, parsing, and display results."""
    file = request.files.get("resume")

    if not file:
        logging.warning("Upload attempted without file.")
        return render_template("index.html", error="No file uploaded. Please select a resume file.")

    filename = file.filename

    if not allowed_file(filename):
        logging.warning(f"Unsupported file type attempted: {filename}")
        return render_template(
            "index.html",
            error="Unsupported file type. Only PDF and DOCX files are allowed."
        )

    # Save uploaded file securely
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(filepath)
        logging.info(f"File saved: {filepath}")
    except Exception as e:
        logging.error(f"Failed to save file: {e}")
        return render_template("index.html", error="Failed to save file. Please try again.")

    # Extract text based on file type
    try:
        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(filepath)
        else:
            text = extract_text_from_docx(filepath)
    except Exception as e:
        logging.error(f"Failed to extract text from file: {e}")
        return render_template("index.html", error="Failed to read the uploaded resume. Please ensure the file is not corrupted.")

    # Clean and parse the resume text
    clean_text_data = clean_text(text)
    parsed_data = parse_resume(clean_text_data)

    logging.info(f"Parsed resume data for file {filename}")

    # Render results in the same page
    return render_template(
        "index.html",
        parsed=parsed_data,
        filename=filename
    )

if __name__ == "__main__":
    app.run(debug=True)
