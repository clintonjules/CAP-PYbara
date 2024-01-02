from flask import Flask, request, jsonify
import os
import sys
from werkzeug.utils import secure_filename
from flask_cors import CORS

sys.path.insert(1, '../')
from model import main as classify_image  # Importing the classify function from your model.py

UPLOAD_FOLDER = '../uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

MODEL_PATH = '../capybara_model.pkl'

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        prediction, prob = classify_image(MODEL_PATH, str(filepath))  # Your model's prediction function
        print("Prediction type:", type(prediction))  # Should be <class 'str'>
        
        prediction_str = str(prediction)
        prob_float = format(prob.item(), ".4f")
        
        prediction_str = "CAP" if prediction_str == "capybara" else "NO CAP"
            
    
        return jsonify({'prediction': prediction_str, 'probability': prob_float})
    else:
        return jsonify("File type not valid")

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
