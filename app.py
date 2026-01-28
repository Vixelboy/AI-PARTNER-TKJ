import streamlit as st
from groq import Groq
import requests
import json
import os

# --- KONFIGURASI FILE & GOOGLE SHEETS ---
MEMORY_FILE = "chat_history_3d.json"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUw0uz4dcpwZzQ6isJiICrlbPo0p_bdnE4UYqXCXKW5EXGyA/formResponse"
ENTRY_ID = "entry.1158580211" 

def lapor_ke_sheets(nama):
    payload = {ENTRY_ID: nama}
    try:
        requests.post(FORM_URL, data=payload, timeout=5)
        return True
    except: return False

def save_memory(messages):
    with open(MEMORY_FILE, "w") as f: json.dump(messages, f)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f: return json.load(f)
    return None

# --- INITIALIZE GROQ ---
client = Groq(api_key="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")

# --- SESSION STATE ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    saved_chats = load_memory()
    st.session_state.messages = saved_chats if saved_chats else [
        {"role": "system", "content": "Anda ahli IT ramah, gunakan bahasa Gen Z dan analogi jaringan."}
    ]

# --- CSS FULL SCREEN 3D (MENGHAPUS HEADER/FOOTER HITAM) ---
def apply_full_3d_style():
    st.markdown("""
    <style>
    /* 1. Menghilangkan Header Hitam & Padding Atas */
    header {visibility: hidden;}
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }
    
    /* 2. Background Full Screen */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
        color: white;
    }

    /* 3. Styling Chat Bubble 3D */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 5px;
    }

    .bubble {
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        font-size: 15px;
        max-width: 85%;
    }

    .user-3d {
        align-self: flex-end;
        background: rgba(0, 150, 255, 0.2);
        border-right: 5px solid #00d2ff;
        box-shadow: 10px 10px 20px rgba(0, 210, 255, 0.1);
    }

    .bot-3d {
        align-self: flex-start;
        background: rgba(255, 255, 255, 0.03);
        border-left: 5px solid #ff00ff;
        box-shadow: -10px 10px 20px rgba(255, 0, 255, 0.1);
    }

    .name-label {
        font-size: 10px;
        font-weight: bold;
        margin-bottom: 8px;
        color: cyan;
        text-shadow: 0 0 5px cyan;
    }
    
    /* 4. Menghilangkan Footer Streamlit */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN MODAL ---
if not st.session_state.user_name:
    st.set_page_config(page_title="Access Point TKJ", page_icon="🔑", layout="wide")
    apply_full_3d_style()
    st.markdown("<h1 style='text-align: center; margin-top: 10vh;'>🖥️ JOIN NETWORK</h1>", unsafe_allow_html=True)
    with st.container():
        _, col, _ = st.columns([1, 2, 1])
        with col:
            with st.form("login"):
                name = st.text_input("Identitas User:")
                btn = st.form_submit_button("CONNECT 🚀")
                if btn and name:
                    lapor_ke_sheets(name)
                    st.session_state.user_name = name
                    st.rerun()
    st.stop()

# --- MAIN APP ---
st.set_page_config(page_title="Digital Agent TKJ 4.0", page_icon="💻", layout="wide")
apply_full_3d_style()

with st.sidebar:
    st.markdown(f"## 👤 {st.session_state.user_name}")
    st.divider()
    if st.button("🗑️ Reset Chat"):
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
    if st.button("🔄 Logout"):
        st.session_state.user_name = None
        st.rerun()

# --- RENDER CHAT ---
st.markdown("<h2 style='text-align: center;'>Digital Agent TKJ 4.0</h2>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        is_user = msg["role"] == "user"
        style = "user-3d" if is_user else "bot-3d"
        name = st.session_state.user_name if is_user else "SERVER AI"
        icon = "👤" if is_user else "🤖"
        
        st.markdown(f"""
        <div class="chat-wrapper">
            <div class="{style} bubble">
                <div class="name-label">{name}</div>
                {icon} {msg['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- INPUT ---
if prompt := st.chat_input("Input command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=st.session_state.messages)
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_memory(st.session_state.messages)
        st.rerun()
    except Exception as e:
        st.error(f"Signal Lost: {e}")
