# <h1 align="center">🏠 Apartment Price Prediction API</h1>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.9-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Flask-3.1.0-green.svg" alt="Flask Version">
  <img src="https://img.shields.io/badge/Google%20Drive%20API-enabled-red.svg" alt="Google Drive API">
</p>

---

## 📝 **Project Description**
The **Apartment Price Prediction API** is a machine learning-powered API built with **Flask**. It predicts the price of apartments in Almaty, Kazakhstan, using multiple models like **Random Forest**, **XGBoost**, **LightGBM**, **CatBoost**, and more. 

The API allows users to submit apartment details in **JSON format** and get an estimated price as the response.

---

## 🚀 **Features**
<ul>
  <li>📦 Supports Multiple Machine Learning Models (RandomForest, XGBoost, CatBoost, LightGBM, etc.)</li>
  <li>🛠️ Preprocessing Pipeline for cleaning and feature engineering</li>
  <li>📈 Predicts Apartment Prices in Real-Time</li>
  <li>🗂️ Uses Google Drive API to dynamically download models</li>
  <li>🔧 Environment Configurations using <code>.env</code> file</li>
</ul>

---

## 🛠️ **Technologies Used**
<ul>
  <li>Python 3.9</li>
  <li>Flask</li>
  <li>Pandas & Numpy</li>
  <li>Scikit-Learn, CatBoost, LightGBM, XGBoost</li>
  <li>Google Drive API</li>
</ul>

---

## 📦 **Project Structure**
```
project/
├── app.py # Main Flask app
├── download_models.py # Script to download models from Google Drive
├── preprocess.py # Preprocessing pipeline for input data
├── models/ # Downloaded models are stored here
├── requirements.txt # Required dependencies
├── .env # Environment variables (API keys, folder IDs, etc.)
├── .gitignore # Ignore venv, models, and large files
└── README.md # Project documentation
```

## 🔥 **How to Run the Project**

<p>Follow the instructions below to get the <strong>API running locally</strong>.</p>

---

<h3>📋 <strong>Step 1: Clone the Repository</strong></h3>
<pre><code>
git clone https://github.com/dexciuq/house-price-prediction-server.git
cd house-price-prediction-server
</code></pre>

---

<h3>📋 <strong>Step 2: Set Up Virtual Environment</strong></h3>
<pre><code>
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate.bat # Windows CMD
</code></pre>

---

<h3>📋 <strong>Step 3: Install Dependencies</strong></h3>
<pre><code>
pip install --no-cache-dir -r requirements.txt
</code></pre>

---

<h3>📋 <strong>Step 4: Set Environment Variables</strong></h3>
<p>Create a <code>.env</code> file in the root of your project with the following variables:</p>

<pre><code>
GOOGLE_DRIVE_API_KEY=your_google_drive_api_key_here
GOOGLE_DRIVE_FOLDER_ID=your_folder_id_here
PORT=5000
DEBUG=True
</code></pre>

---

<h3>📋 <strong>Step 5: Run the API</strong></h3>
<pre><code>
python app.py
</code></pre>

<p>The API will be running at:</p>
<pre><code>http://localhost:5000/</code></pre>

---

<h2>📡 <strong>API Endpoints</strong></h2>

<table>
  <tr>
    <th>Endpoint</th>
    <th>Method</th>
    <th>Description</th>
    <th>Example</th>
  </tr>
  <tr>
    <td><code>/healthcheck</code></td>
    <td>GET</td>
    <td>Check if API is running</td>
    <td><code>/healthcheck</code></td>
  </tr>
  <tr>
    <td><code>/predict</code></td>
    <td>POST</td>
    <td>Predict the price of an apartment</td>
    <td><code>/predict?model=catboost</code></td>
  </tr>
</table>

---

<h2>💡 <strong>How to Make Predictions</strong></h2>

<p>To make predictions, send a <strong>POST request</strong> to the <code>/predict</code> endpoint with apartment data in <strong>JSON</strong> format.</p>

<h3>🔥 <strong>Request Example</strong></h3>

<pre><code>
{
    "square_m": 47,
    "rooms": 1,
    "floor": 1,
    "total_floors": 4,
    "year_built": 2014,
    "balcony": null,
    "bathroom": null,
    "ceiling_height_m": 2.8,
    "house_material": "монолитный",
    "condition": "свежий ремонт",
    "furniture_status": null,
    "security": null,
    "is_pledged": false,
    "was_former_hostel": false,
    "country": "Kazahstan",
    "city": "Almaty",
    "district": "Alatauskiy_r-n",
    "microdistrict": "mkr_Zerdeli_(Algabas-6)",
    "street": "Mkr_Zerdeli_(Algabas-6)",
    "house_num": "79",
    "lat": 43.279281,
    "lon": 76.826456
}
</code></pre>

<p><strong>URL</strong>: <code>http://localhost:5000/predict?model=catboost</code></p>

<h3>📡 <strong>cURL Request</strong></h3>

<pre><code>
curl -X POST http://localhost:5000/predict?model=catboost \
-H "Content-Type: application/json" \
-d '{
    "square_m": 47,
    "rooms": 1,
    "floor": 1,
    "total_floors": 4,
    "year_built": 2014,
    "balcony": null,
    "bathroom": null,
    "ceiling_height_m": 2.8,
    "house_material": "монолитный",
    "condition": "свежий ремонт",
    "furniture_status": null,
    "security": null,
    "is_pledged": false,
    "was_former_hostel": false,
    "country": "Kazahstan",
    "city": "Almaty",
    "district": "Alatauskiy_r-n",
    "microdistrict": "mkr_Zerdeli_(Algabas-6)",
    "street": "Mkr_Zerdeli_(Algabas-6)",
    "house_num": "79",
    "lat": 43.279281,
    "lon": 76.826456
}'
</code></pre>

---

<h2>🧪 <strong>Example Response</strong></h2>

<p>If successful, you will receive a JSON response with the predicted price:</p>

<pre><code>
{
    "predicted_price": 25000000
}
</code></pre>

> **Note:** The price is returned in **KZT (Kazakhstani Tenge)**.

---

<h2>🛠️ <strong>Environment Variables</strong></h2>

<p>Environment variables are stored in a <code>.env</code> file. Here’s what you need to add to the file:</p>

<pre><code>
GOOGLE_DRIVE_API_KEY=your_google_drive_api_key_here
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id_here
PORT=5000
DEBUG=True
</code></pre>

---

<h2>🚀 <strong>Deployment</strong></h2>

<p>To deploy the app, you can use <strong>Docker</strong> or <strong>Docker-Compose</strong>.</p>

<h3>📦 <strong>Docker</strong></h3>

<h4>Step 1: Build Docker Image</h4>
<pre><code>
docker build -t apartment-price-api .
</code></pre>

<h4>Step 2: Run Docker Container</h4>
<pre><code>
docker run -p 5000:5000 --env-file .env apartment-price-api
</code></pre>

<p>Access the API at:</p>
<pre><code>http://localhost:5000</code></pre>

---

<h2>📧 <strong>Contact</strong></h2>

<p>If you have any questions or issues, please feel free to reach out at:</p>

<p>📧 <strong>Email</strong>: <a href="mailto:dimokzhasulanov@gmail.com">dimokzhasulanov@gmail.com</a></p>
<p>🌐 <strong>GitHub</strong>: <a href="https://github.com/dexciuq" target="_blank">dexciuq</a></p>

---

<p align="center">Made with ❤️ by <strong>Dinmukhammed, Nurdaulet, Bekarys</strong></p>
