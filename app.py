import streamlit as st
from groq import Groq
import requests
import json
import os

# --- 1. KONFIGURASI FILE & GOOGLE SHEETS ---
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

# --- 2. INITIALIZE GROQ ---
client = Groq(api_key="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")

# --- 3. SESSION STATE ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    saved_chats = load_memory()
    st.session_state.messages = saved_chats if saved_chats else [
        {"role": "system", "content": "Anda ahli IT ramah, gunakan bahasa Gen Z dan analogi jaringan."}
    ]

# --- 4. CSS GLASSMORPHISM 3D (THE MAGIC) ---
def apply_3d_style():
    st.markdown("""
    <style>
    /* Background Animasi */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* Container Chat 3D */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 10px;
    }

    /* Efek Kaca (Glassmorphism) */
    .bubble {
        padding: 15px 20px;
        border-radius: 25px;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        font-size: 15px;
        max-width: 80%;
        color: white;
    }

    /* Bubble User - Melayang Biru */
    .user-3d {
        align-self: flex-end;
        background: rgba(0, 123, 255, 0.25);
        border-right: 4px solid #00d2ff;
        box-shadow: 5px 5px 15px rgba(0, 210, 255, 0.2);
    }

    /* Bubble Bot - Melayang Gelap */
    .bot-3d {
        align-self: flex-start;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ff00ff;
        box-shadow: -5px 5px 15px rgba(255, 0, 255, 0.2);
    }

    .name-label {
        font-size: 10px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        color: rgba(255,255,255,0.6);
    }
    
    /* Tombol & Input 3D */
    .stButton>button {
        border-radius: 12px;
        border: none;
        background: linear-gradient(145deg, #1e1e3f, #2b2b5a);
        box-shadow: 6px 6px 12px #0a0a14, -6px -6px 12px #26264e;
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LOGIN MODAL ---
if not st.session_state.user_name:
    st.set_page_config(page_title="Access Point TKJ", page_icon="🔑")
    apply_3d_style()
    st.markdown("<h1 style='text-align: center; color: white;'>🖥️ JOIN NETWORK</h1>", unsafe_allow_html=True)
    with st.form("login"):
        name = st.text_input("Identitas User:")
        btn = st.form_submit_button("CONNECT 🚀")
        if btn and name:
            lapor_ke_sheets(name)
            st.session_state.user_name = name
            st.rerun()
    st.stop()

# --- 6. MAIN APP ---
st.set_page_config(page_title="Digital Agent TKJ 4.0", page_icon="💻")
apply_3d_style()

with st.sidebar:
    st.markdown(f"### 👤 Active User: {st.session_state.user_name}")
    if st.button("🗑️ Clear History"):
        if os.path.exists(MEMORY_FILE): os.remove(MEMORY_FILE)
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()
    if st.button("🔄 Logout"):
        st.session_state.user_name = None
        st.rerun()

st.title("Digital Agent TKJ 4.0")
st.caption("UI Prototype: 3D Glassmorphism Edition")

# --- 7. RENDER CHAT ---
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

# --- 8. INPUT ---
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
