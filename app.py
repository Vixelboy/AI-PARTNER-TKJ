import streamlit as st
from groq import Groq
import requests
import json
import os
from datetime import datetime

# --- 1. INITIALIZE SESSION STATE (Paling Atas biar Gak Error) ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda ahli IT ramah, gunakan bahasa Gen Z dan analogi jaringan."}
    ]

# --- 2. KONFIGURASI FILE & GOOGLE SHEETS ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUw0uz4dcpwZzQ6isJiICrlbPo0p_bdnE4UYqXCXKW5EXGyA/formResponse"
ENTRY_ID = "entry.1158580211" 

def lapor_ke_sheets(nama):
    payload = {ENTRY_ID: nama}
    try: requests.post(FORM_URL, data=payload, timeout=5)
    except: pass

def save_chat_to_file():
    # Simpan riwayat berdasarkan nama user
    if st.session_state.user_name:
        filename = f"history_{st.session_state.user_name}.json"
        with open(filename, "w") as f:
            json.dump(st.session_state.messages, f)

# --- 3. CSS FULL 3D GLASSMORPHISM ---
def apply_ui():
    st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
        color: white;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Chat Bubble 3D */
    .bubble {
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 15px;
        max-width: 85%;
    }
    .user-style { align-self: flex-end; background: rgba(0, 150, 255, 0.2); border-right: 5px solid #00d2ff; }
    .bot-style { align-self: flex-start; background: rgba(255, 255, 255, 0.03); border-left: 5px solid #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. LOGIC LOGIN ---
if not st.session_state.user_name:
    st.set_page_config(page_title="Join Network", layout="centered")
    apply_ui()
    st.markdown("<h1 style='text-align: center;'>🖥️ JOIN NETWORK</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        name = st.text_input("Input Identity:")
        if st.form_submit_button("CONNECT 🚀"):
            if name:
                lapor_ke_sheets(name)
                st.session_state.user_name = name
                st.rerun()
    st.stop()

# --- 5. MAIN APP (Dijalankan jika sudah login) ---
st.set_page_config(page_title="Digital Agent TKJ", layout="wide")
apply_ui()
client = Groq(api_key="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")

# SIDEBAR ALA GEMINI
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.user_name}")
    if st.button("➕ Chat Baru"):
        st.session_state.messages = [{"role": "system", "content": "..."}]
        st.rerun()
    
    st.write("---")
    st.markdown("🕒 **Riwayat Chat**")
    # Cek file riwayat
    if os.path.exists(f"history_{st.session_state.user_name}.json"):
        if st.button(f"📄 Sesi Terakhir {st.session_state.user_name}"):
            with open(f"history_{st.session_state.user_name}.json", "r") as f:
                st.session_state.messages = json.load(f)
            st.rerun()
            
    st.write("---")
    theme = st.selectbox("Ganti Vibe:", ["Space Dark", "Cyber Neon", "Kawaii"])
    if st.button("🔄 Logout"):
        st.session_state.user_name = None
        st.rerun()

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
                <small style="color: cyan;">{label}</small><br>{msg['content']}
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
