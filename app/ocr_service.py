from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os
import platform

# Set Tesseract path conditionally based on platform
if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# For Linux/MacOS, no need to set path if installed properly

def process_pdf(pdf_path):
    """Convert PDF to images and process OCR on each page."""
    try:
        # Ensure absolute path is used
        pdf_path = os.path.abspath(pdf_path)

        # For Windows: Use poppler_path parameter if needed
        if platform.system() == 'Windows':
            from pdf2image.exceptions import PDFInfoNotInstalledError
            try:
                # Try with default settings first
                images = convert_from_path(pdf_path)
            except PDFInfoNotInstalledError:
                # If poppler is not in PATH, provide a helpful error
                return "Error: Poppler not installed. Please install poppler for PDF processing."
        else:
            images = convert_from_path(pdf_path)

        if not images:
            return "No pages found in PDF."
    except Exception as e:
        return f"Error converting PDF to images: {e}"

    text_output = []

    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        text_output.append(f"Page {i + 1}:\n{text}")

    return "\n".join(text_output)


def process_image(image_path):
    """Process image with OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Simple tagging for demonstration
        tagged_text = tag_content(text)

        return text.strip() if text.strip() else "No readable text found in image.", tagged_text
    except Exception as e:
        return f"Error processing image: {e}", f"<p>Error: {e}</p>"


def tag_content(text):
    """Add basic semantic tagging to the extracted text."""
    if not text.strip():
        return "<p>No content to tag</p>"

    # Very basic tagging - this could be much more sophisticated
    paragraphs = text.split('\n\n')
    tagged = []

    for i, para in enumerate(paragraphs):
        if i == 0 and len(para) < 100:  # Likely a title
            tagged.append(f'<h1 class="title">{para}</h1>')
        elif len(para) < 50 and para.endswith(':'):  # Likely a section header
            tagged.append(f'<h2 class="section">{para}</h2>')
        else:
            # Simple paragraph
            tagged.append(f'<p>{para}</p>')

    return ''.join(tagged)


def process_file(file_path):
    """Determine whether to process an image or PDF."""
    if file_path.lower().endswith(".pdf"):
        text = process_pdf(file_path)
        tagged_text = tag_content(text)
        return text, tagged_text
    else:
        return process_image(file_path)