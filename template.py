import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "resumeParser"

list_of_files = [
    f"{project_name}/__init__.py",
    f"{project_name}/parser.py",
    f"{project_name}/utils.py",
    f"{project_name}/pdf_reader.py",
    "data/.gitkeep",
    "outputs/resume_outputs.json",
    "tests/test_parser.py",
    "tests/test_pdf_reader.py",
    "research/trails.ipynb",
    "app.py",
    "requirements.txt",
    "setup.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # creates an empty file
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
