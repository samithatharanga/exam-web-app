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
    /* UPLOAD SECTION - GLASSMORPHISM CARD */
    /* ─────────────────────────────────────────────────────────────────── */
    .upload-container {
        padding: 40px 30px;
        border-radius: 20px;
        background: rgba(20, 20, 40, 0.4);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1.5px solid rgba(0, 212, 255, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 212, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        margin: 30px 0;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .upload-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
        transition: left 0.5s ease-in-out;
    }
    
    .upload-container:hover {
        border: 1.5px solid rgba(0, 212, 255, 0.5);
        box-shadow: 
            0 12px 48px rgba(0, 212, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        background: rgba(20, 20, 40, 0.6);
    }
    
    .upload-container:hover::before {
        left: 100%;
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
    
    .footer-text a {
        color: #00d4ff;
        text-decoration: none;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .footer-text a:hover {
        color: #7c3aed;
        text-shadow: 0 0 15px rgba(0, 212, 255, 0.5);
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
    
    /* ────────────────────────────────────────────────
