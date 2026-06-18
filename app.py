import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json

# 1. Page Configuration (අනිවාර්යයෙන්ම Code එකේ උඩින්ම තියෙන්න ඕනේ)
st.set_page_config(
    page_title="RPS AI Referee",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS (Glassmorphism සහ Premium පෙනුම සඳහා)
st.markdown("""
    <style>
    .prediction-box {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 40px !important;
        margin-bottom: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Chatbot-style Introduction (AI කෙනෙක් කතා කරනවා වගේ)
with st.chat_message("assistant", avatar="🤖"):
    st.markdown("<p class='main-title'>👋 Hello! I am your AI Referee.</p>", unsafe_allow_html=True)
    st.markdown("Let's play **Rock, Paper, Scissors**! ✂️🪨📄")
    st.markdown("""
    I don't need pictures of real rocks or scissors. I want to see **YOUR HAND**! 
    
    **How to play:**
    1. 📸 Take a clear photo of your hand showing **✊ Rock**, **✋ Paper**, or **✌️ Scissors**.
    2. 📤 Upload it below.
    3. 🧠 My AI brain will guess your move instantly!
    """)

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
    st.error(f"⚠️ Error loading model files. Details: {e}")
    st.stop()

st.divider()

# Image Uploader Setup
uploaded_file = st.file_uploader("Drop your hand photo here...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert('RGB')
    
    # User ගේ පැත්තෙන් අහනවා වගේ පෙන්වීම
    with st.chat_message("user", avatar="👤"):
        st.write("**Here is my move!**")
        # ෆොටෝ එක මැදින් ලස්සනට පෙන්නන්න Columns පාවිච්චි කිරීම
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.image(image, caption='Your Uploaded Hand Photo', use_column_width=True)

    # AI ගේ පැත්තෙන් උත්තර දීම
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing your hand shape... 🧐"):
            # Preprocess the image to match new model input requirements (160x160)
            img = image.resize((160, 160))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0) # Create a batch of 1

            # Make Prediction
            predictions = model.predict(img_array)
            predicted_class_idx = np.argmax(predictions[0])
            predicted_class = class_names[predicted_class_idx]
            confidence = np.max(predictions[0]) * 100

        # අදාළ අයිකන් එක තේරීම
        predicted_lower = predicted_class.lower()
        if "rock" in predicted_lower:
            emoji = "✊"
        elif "paper" in predicted_lower:
            emoji = "✋"
        elif "scissor" in predicted_lower:
            emoji = "✌️"
        else:
            emoji = "✨"
        
        # ලස්සන Glass Box එකක Result එක පෙන්වීම
        st.markdown(f"""
        <div class="prediction-box">
            <h4 style="margin-bottom:0; color: #888;">My Prediction:</h4>
            <h1 style="font-size: 55px; margin-top:0;">{emoji} {predicted_class.upper()}</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress bar එකක් මගින් Confidence එක පෙන්වීම
        st.write(f"**AI Confidence Level:** {confidence:.2f}%")
        st.progress(int(confidence))
        
        # Confidence එක අනුව වෙනස් වෙන Messages
        if confidence > 90:
            st.success("I am very confident about this! 😎")
        elif confidence > 70:
            st.info("I'm pretty sure, but your hand shape is a bit tricky! 🤔")
        else:
            st.warning("I'm just guessing... make sure your hand is clear in the photo! 😅")
