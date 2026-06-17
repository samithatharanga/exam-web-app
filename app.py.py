import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json

# Page Configuration
st.set_page_config(page_title="AI Fruit Classification", page_icon="🍎", layout="centered")

st.title("🍎 AI Fruit Classification App")
st.write("Upload an image of a fruit, and the AI model will classify it using MobileNetV2 Transfer Learning.")

# Load the trained Keras model (Cached to load only once)
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("student_mobilenetv2_transfer_learning.keras")

# Load the class names from JSON
@st.cache_data
def load_class_names():
    with open("class_names.json", "r") as f:
        return json.load(f)

# Initialize Model and Class Names
try:
    model = load_model()
    class_names = load_class_names()
except Exception as e:
    st.error(f"Error loading model files. Make sure the .keras and .json files are in the repository. Details: {e}")
    st.stop()

# Image Uploader Setup
uploaded_file = st.file_uploader("Upload a fruit image (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    with st.spinner("Classifying the image..."):
        # Preprocess the image to match model input requirements
        img = image.resize((224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch of 1

        # Make Prediction
        predictions = model.predict(img_array)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = class_names[predicted_class_idx]
        confidence = np.max(predictions[0]) * 100

        # Display Results
        st.success(f"### **Prediction:** {predicted_class}")
        st.info(f"**Confidence Level:** {confidence:.2f}%")