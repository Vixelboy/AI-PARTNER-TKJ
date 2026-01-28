import streamlit as st
from groq import Groq
import requests
import json
import os
from datetime import datetime

# --- 1. INITIALIZE SESSION STATE ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah Ahli IT paham coding, sistem, jaringan, komputer yang ahli dan ramah. Gunakan analogi jaringan dan pakai bahasa Gen z."}
    ]

# --- 2. KONFIGURASI GOOGLE FORM ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUw0uz4dcpwZzQ6isJiICrlbPo0p_bdnE4UYqXCXKW5EXGyA/formResponse"
ENTRY_ID = "entry.1158580211" 

def lapor_ke_sheets(nama):
    payload = {ENTRY_ID: nama}
    try: requests.post(FORM_URL, data=payload, timeout=5)
    except: pass

def save_chat_to_file():
    if st.session_state.user_name:
        filename = f"history_{st.session_state.user_name}.json"
        with open(filename, "w") as f:
            json.dump(st.session_state.messages, f)

# --- 3. CSS DYNAMIC THEME (FIX THEME NOT CHANGING) ---
def apply_ui(theme):
    # Logika Warna Berdasarkan Tema
    if theme == "Cyber Neon":
        bg = "linear-gradient(135deg, #000428, #004e92)"
        u_glow, b_glow = "#00f2ff", "#ff00ff"
        u_bg, b_bg = "rgba(0, 242, 255, 0.1)", "rgba(255, 0, 255, 0.1)"
    elif theme == "Kawaii":
        bg = "linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)"
        u_glow, b_glow = "#ff6b6b", "#f06292"
        u_bg, b_bg = "rgba(255, 107, 107, 0.2)", "rgba(240, 98, 146, 0.2)"
    else: # Space Dark
        bg = "linear-gradient(135deg, #0f0c29, #302b63, #24243e)"
        u_glow, b_glow = "#00d2ff", "#ff00ff"
        u_bg, b_bg = "rgba(0, 210, 255, 0.1)", "rgba(255, 0, 255, 0.05)"

    st.markdown(f"""
    <style>
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stApp {{
        background: {bg};
        background-attachment: fixed;
        color: white;
    }}
    [data-testid="stSidebar"] {{
        background: rgba(15, 12, 41, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}
    .bubble {{
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        max-width: 85%;
    }}
    .user-style {{ 
        align-self: flex-end; 
        background: {u_bg}; 
        border-right: 5px solid {u_glow}; 
        box-shadow: 0 0 15px {u_glow}44;
    }}
    .bot-style {{ 
        align-self: flex-start; 
        background: {b_bg}; 
        border-left: 5px solid {b_glow}; 
        box-shadow: 0 0 15px {b_glow}44;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIC LOGIN ---
if not st.session_state.user_name:
    st.set_page_config(page_title="Join Network", layout="centered")
    apply_ui("Space Dark") # Default login theme
    st.markdown("<h1 style='text-align: center;'>🖥️ JOIN NETWORK</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        name = st.text_input("Input Identity:")
        if st.form_submit_button("CONNECT 🚀"):
            if name:
                lapor_ke_sheets(name)
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# --- 5. MAIN APP ---
st.set_page_config(page_title="Digital Agent TKJ", layout="wide")

# SIDEBAR (Ambil input tema dulu sebelum apply UI)
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    theme_choice = st.selectbox("Ganti Vibe:", ["Space Dark", "Cyber Neon", "Kawaii"])
    
    if st.button("➕ Chat Baru"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
    
    st.write("---")
    if st.button("🔄 Logout"):
        st.session_state.user_name = None
        st.rerun()

# Apply UI berdasarkan pilihan di sidebar
apply_ui(theme_choice)

client = Groq(api_key="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")

# RENDER CHAT
st.markdown(f"<h3 style='text-align: center;'>Digital Agent TKJ 4.0</h3>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        is_user = msg["role"] == "user"
        style = "user-style" if is_user else "bot-style"
        label = st.session_state.user_name if is_user else "SERVER AI"
        st.markdown(f"""
        <div style="display: flex; flex-direction: column;">
            <div class="bubble {style}">
                <small style="color: {'cyan' if is_user else '#ff00ff'}; font-weight: bold;">{label}</small><br>{msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# INPUT
if prompt := st.chat_input("Tanya apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        res = client.chat.completions.create(model="llama-3.1-8b-instant", messages=st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": res.choices[0].message.content})
        save_chat_to_file()
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
