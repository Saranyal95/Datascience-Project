import streamlit as st
import joblib
import numpy as np
from PIL import Image
import io
import base64

# Load the trained model
model = joblib.load('xgboost_model.pkl')

# Function to convert image to base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Specify the path to your local image
image_path = r"C:\Users\itsej\Downloads\solar.jpg"  # Use raw string or double backslashes

# Convert image to base64
img_base64 = image_to_base64(image_path)

# Apply CSS to set the background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        height: 100vh;
    }}
    .css-1v3fvcr, .css-1a2j5i7 {{
        background-color: rgba(0, 0, 0, 0.5); /* Dark overlay for better readability */
    }}
    .stTextInput, .stNumberInput, .stButton {{
        color: #eb856e;
        background-color: #2d2d2d;
        font-size: 20px;
        border: 1px solid #444;
    }}
    .stSlider {{
        color: #eb856e;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title('Solar Power Generation Prediction')

# Collect user inputs for environmental variables
distance_to_solar_noon = st.number_input('Distance to Solar Noon (radians)', value=0.5)
temperature = st.number_input('Temperature (°C)', value=25.0)
wind_direction = st.number_input('Wind Direction (degrees)', value=180)
wind_speed = st.number_input('Wind Speed (m/s)', value=5.0)
sky_cover = st.slider('Sky Cover (0=Clear, 4=Covered)', 0, 4, value=2)
visibility = st.number_input('Visibility (km)', value=10.0)
humidity = st.number_input('Humidity (%)', value=50)
average_wind_speed = st.number_input('Average Wind Speed (m/s)', value=5.0)
average_pressure = st.number_input('Average Pressure (mercury inches)', value=29.92)

# Prepare input data
input_data = np.array([[distance_to_solar_noon, temperature, wind_direction, wind_speed,
                        sky_cover, visibility, humidity, average_wind_speed, average_pressure]])

# Predict button
if st.button('Predict'):
    prediction = model.predict(input_data)
    st.write(f'Predicted Power Generated: {prediction[0]:.2f} Joules')
