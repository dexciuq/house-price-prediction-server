import os
import logging
import joblib
from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from flask_cors import CORS 
from dotenv import load_dotenv
from download import download_all_models_from_folder
from preprocess import preprocess_input

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
CORS(app)
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Load all models dynamically from the /models folder
models = {}
models_dir = 'models'

try:
    for filename in os.listdir(models_dir):
        if filename.endswith('.pkl'):
            model_name = filename.split('_model.pkl')[0]
            model_path = os.path.join(models_dir, filename)
            models[model_name] = joblib.load(model_path)
            logger.info(f"Loaded model: {model_name} from {model_path}")
except Exception as e:
    logger.error(f"Error loading models: {e}")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    try:
        server_info = {
            "status": "ok",
            "server": "Apartment Price Prediction API",
            "models_loaded": list(models.keys())
        }
        return jsonify(server_info), 200
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


@app.route('/predict', methods=['POST'])
def predict():
    try:
        model_name = request.args.get('model', 'linear_regression')
        if model_name == 'all':
            selected_models = models.values()
        elif model_name in models:
            selected_models = [models[model_name]]
        else:
            return jsonify({"error": "Model not found"}), 400

        # Check if request has a JSON body
        if not request.is_json:
            return jsonify({"error": "Invalid request. JSON body required."}), 400

        input_data = request.get_json()
        data = pd.DataFrame([input_data])

        try:
            preprocessed_data = preprocess_input(data)
        except ValueError as e:
            return jsonify({"error": "Preprocessing error", "message": str(e)}), 400
      
        predictions = [model.predict(preprocessed_data)[0] for model in selected_models]
        avg_predicted_price = round(float(np.mean(predictions)), 2) * 1e6

        return jsonify({"predicted_price": avg_predicted_price}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == '__main__':
    if not os.path.exists('models'):
        os.makedirs('models')
        logger.info("Created 'models' directory.")

    if not os.listdir('models'):
        FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        logger.info(f"Downloading models from Google Drive folder: {FOLDER_ID}")
        download_all_models_from_folder(FOLDER_ID)
    else:
        logger.info("Models already exist. Skipping download.")
        
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
