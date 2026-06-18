import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import time

# ═══════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION (Must be at the very top)
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RPS AI Referee",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 2. HIDE STREAMLIT DEFAULT UI (Header, Footer, Hamburger Menu, Whitespace)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* Hide Streamlit default header, footer, and menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Remove top padding and margins */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Pure OLED-friendly black background */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #000000 !important;
        background: #000000 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 3. ULTRA-PREMIUM CYBER-GLASSMORPHISM CSS STYLING
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <style>
    /* ─────────────────────────────────────────────────────────────────── */
    /* GLOBAL TEXT & TYPOGRAPHY STYLING */
    /* ─────────────────────────────────────────────────────────────────── */
    * {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", 
                     "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif !important;
    }
    
    p, span, div {
        color: #e8e8ff !important;
        letter-spacing: 0.3px;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* MAIN TITLE - GLOWING NEON EFFECT */
    /* ─────────────────────────────────────────────────────────────────── */
    .main-title {
        font-size: 48px !important;
        font-weight: 700 !important;
        margin: 0 !important;
        background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 50%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
        animation: neon-flicker 3s ease-in-out infinite;
    }
    
    @keyframes neon-flicker {
        0%, 100% {
            text-shadow: 0 0 20px rgba(0, 212, 255, 0.4), 0 0 40px rgba(124, 58, 237, 0.3);
        }
        50% {
            text-shadow: 0 0 30px rgba(0, 212, 255, 0.6), 0 0 60px rgba(124, 58, 237, 0.5);
        }
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* FILE UPLOADER - CUSTOM STYLING (THE UNIFIED BOX) */
    /* ─────────────────────────────────────────────────────────────────── */
    /* We style the native Streamlit Dropzone to be the beautiful Glass box */
    [data-testid="stFileUploadDropzone"] {
        background: rgba(20, 20, 40, 0.4) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 2px dashed rgba(0, 212, 255, 0.4) !important;
        border-radius: 20px !important;
        padding: 40px 20px !important;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    [data-testid="stFileUploadDropzone"]:hover {
        background: rgba(20, 20, 40, 0.7) !important;
        border: 2px solid rgba(0, 212, 255, 0.8) !important;
        box-shadow: 0 12px 48px rgba(0, 212, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* PREDICTION BOX - DRAMATIC REVEAL WITH GLOW */
    /* ─────────────────────────────────────────────────────────────────── */
    .prediction-box {
        padding: 50px 40px;
        border-radius: 25px;
        background: rgba(10, 10, 25, 0.5);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 2px solid rgba(124, 58, 237, 0.4);
        text-align: center;
        box-shadow: 
            0 0 60px rgba(124, 58, 237, 0.3),
            0 0 100px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        margin: 40px 0;
        animation: prediction-entrance 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes prediction-entrance {
        0% {
            opacity: 0;
            transform: scale(0.8) translateY(20px);
            filter: blur(10px);
        }
        100% {
            opacity: 1;
            transform: scale(1) translateY(0);
            filter: blur(0);
        }
    }
    
    .prediction-box::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(124, 58, 237, 0.1) 0%, transparent 70%);
        animation: glow-pulse 4s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes glow-pulse {
        0%, 100% {
            transform: scale(1);
            opacity: 0.5;
        }
        50% {
            transform: scale(1.2);
            opacity: 0.8;
        }
    }
    
    .prediction-box h1 {
        font-size: 80px !important;
        margin: 20px 0 0 0 !important;
        color: #00d4ff !important;
        text-shadow: 
            0 0 20px rgba(0, 212, 255, 0.8),
            0 0 40px rgba(124, 58, 237, 0.5);
        animation: float-up 2s ease-in-out infinite;
        position: relative;
        z-index: 1;
    }
    
    @keyframes float-up {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .prediction-box h4 {
        color: #a0a0d0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* CONFIDENCE METER - SLEEK PROGRESS BAR */
    /* ─────────────────────────────────────────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #7c3aed 0%, #00d4ff 100%) !important;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.4) !important;
        height: 8px !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* CHAT MESSAGE STYLING - PREMIUM DARK MODE */
    /* ─────────────────────────────────────────────────────────────────── */
    .stChatMessage {
        background: transparent !important;
        padding: 16px 0 !important;
    }
    
    .stChatMessageContent {
        background: rgba(25, 25, 50, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(0, 212, 255, 0.15) !important;
        padding: 20px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* SUCCESS & INFO MESSAGES - NEON ALERTS */
    /* ─────────────────────────────────────────────────────────────────── */
    .stSuccess {
        background: rgba(0, 212, 255, 0.08) !important;
        border-left: 4px solid #00d4ff !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        box-shadow: 0 0 20px rgba(0, 212, 255, 0.15) !important;
    }
    
    .stInfo {
        background: rgba(124, 58, 237, 0.08) !important;
        border-left: 4px solid #7c3aed !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.15) !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.08) !important;
        border-left: 4px solid #ffa500 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        box-shadow: 0 0 20px rgba(255, 165, 0, 0.15) !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* DIVIDER - SUBTLE GLOW */
    /* ─────────────────────────────────────────────────────────────────── */
    hr {
        border: 0 !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.3), transparent) !important;
        margin: 30px 0 !important;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* IMAGE CAPTION - SUBTLE & ELEGANT */
    /* ─────────────────────────────────────────────────────────────────── */
    .stImage {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 212, 255, 0.15);
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* FOOTER SECTION - PREMIUM DEVELOPER CREDITS */
    /* ─────────────────────────────────────────────────────────────────── */
    .footer-container {
        margin-top: 80px;
        padding-top: 40px;
        border-top: 1px solid rgba(0, 212, 255, 0.15);
        text-align: center;
    }
    
    .footer-text {
        font-size: 13px;
        color: #808099;
        letter-spacing: 1px;
        font-weight: 500;
    }
    
    .developer-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin: 15px 0;
    }
    
    .developer-name {
        color: #e8e8ff;
        font-weight: 600;
        font-size: 14px;
    }
    
    .separator {
        color: #404055;
        font-weight: 300;
    }
    
    .powered-by {
        margin-top: 15px;
        font-size: 12px;
        color: #606070;
    }
    
    .powered-by strong {
        color: #00d4ff;
    }
    
    /* ─────────────────────────────────────────────────────────────────── */
    /* LOADING SPINNER ENHANCEMENT */
    /* ─────────────────────────────────────────────────────────────────── */
    .stSpinner {
        color: #00d4ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 4. LOAD MODEL & CLASS NAMES (Cached - unchanged logic)
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("student_mobilenetv2_transfer_learning.keras")

@st.cache_data
def load_class_names():
    with open("class_names.json", "r") as f:
        return json.load(f)

try:
    model = load_model()
    class_names = load_class_names()
except Exception as e:
    st.error(f"⚠️ Error loading model files. Details: {e}")
    st.stop()

# ═══════════════════════════════════════════════════════════════════════════════
# 5. MAIN TITLE WITH NEON GLOW EFFECT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<p class='main-title'>👋 AI Referee</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; color: #a0a0d0; letter-spacing: 1px; margin-top: -20px;'>Rock • Paper • Scissors</p>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 6. INTRODUCTION WITH CHATBOT VIBES
# ═══════════════════════════════════════════════════════════════════════════════
with st.chat_message("assistant", avatar="🤖"):
    st.markdown("""
    **Welcome to the future of hand gesture recognition!** 🚀
    
    I'm your AI Referee, powered by advanced computer vision. I analyze hand shapes in real-time to predict your move.
    """)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# 7. UPLOAD SECTION WITH ENHANCED UX (UNIFIED BOX)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <h3 style="color: #00d4ff; margin: 0 0 10px 0; font-size: 24px;">📸 Show Me Your Hand!</h3>
        <p style="color: #a0a0d0; font-size: 15px; margin: 5px 0;">
            Upload a <strong>clear photo</strong> of your hand showing:
        </p>
        <p style="color: #808099; font-size: 15px; letter-spacing: 1px;">
            ✊ <span style="color: #e8e8ff;">ROCK</span> &nbsp;&nbsp;|&nbsp;&nbsp; ✋ <span style="color: #e8e8ff;">PAPER</span> &nbsp;&nbsp;|&nbsp;&nbsp; ✌️ <span style="color: #e8e8ff;">SCISSORS</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 8. IMAGE UPLOADER (Now styling makes it the single glowing box)
# ═══════════════════════════════════════════════════════════════════════════════
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# ═══════════════════════════════════════════════════════════════════════════════
# 9. PREDICTION LOGIC WITH DRAMATIC REVEALS
