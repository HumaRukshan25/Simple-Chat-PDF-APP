import os
from flask import Flask, request, render_template
from pdf_processing import extract_text_from_pdf
from question_answering import answer_question

app = Flask(__name__)

# Define the path to the temporary directory
TEMP_DIR = 'temp'  # Update this path as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['post'])
def upload():
    uploaded_file = request.files['pdf_file']
    if uploaded_file.filename != '':
        # Ensure the temporary directory exists
        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        # Save the uploaded file to the temporary location
        pdf_path = os.path.join(TEMP_DIR, uploaded_file.filename)
        uploaded_file.save(pdf_path)

        try:
            # Extract text from the saved PDF file
            pdf_text = extract_text_from_pdf(pdf_path)
        except PermissionError:
            pdf_text = 'Error: The PDF file is still in use. Please make sure no other programs are using it.'

        # Remove the temporary file (if it's not in use)
        try:
            os.remove(pdf_path)
        except PermissionError:
            pass

        return pdf_text
    return 'No PDF file provided'

@app.route('/ask', methods=['POST'])
def ask():
    pdf_text = request.form['pdf_text']
    question = request.form['question']
    answer = answer_question(pdf_text, question)
    return answer

if __name__ == '__main__':
    app.run(debug=True)