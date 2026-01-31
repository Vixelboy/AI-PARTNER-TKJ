import streamlit as st
from groq import Groq
import requests
import json
import os

# --- 1. KONFIGURASI HALAMAN (WAJIB PALING ATAS) ---
st.set_page_config(page_title="Digital Agent TKJ", page_icon="💻")

# --- 2. SETUP API KEY ---
# ✅ API Key baru sudah dimasukkan di sini
GROQ_API_KEY = "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" 

client = Groq(api_key=GROQ_API_KEY)

# --- 3. FUNGSI MEMORY & GOOGLE SHEETS ---
MEMORY_FILE = "chat_history.json"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScUw0uz4dcpwZzQ6isJiICrlbPo0p_bdnE4UYqXCXKW5EXGyA/formResponse"
ENTRY_ID = "entry.1158580211" 

def save_memory(messages):
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f)

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return None

def lapor_ke_sheets(nama):
    payload = {ENTRY_ID: nama}
    try:
        requests.post(FORM_URL, data=payload, timeout=5)
        return True
    except:
        return False

# --- 4. INISIALISASI SESSION STATE ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "messages" not in st.session_state:
    saved_chats = load_memory()
    if saved_chats:
        st.session_state.messages = saved_chats
    else:
        st.session_state.messages = [
            {"role": "system", "content": "Anda adalah Ahli IT paham coding, sistem, jaringan, komputer yang ahli dan ramah, pakai bahasa Gen z."}
        ]

# --- 5. HALAMAN LOGIN (JIKA BELUM ADA NAMA) ---
if not st.session_state.user_name:
    st.title("👋 Welcome to Digital Agent TKJ")
    with st.form("name_form"):
        name_input = st.text_input("Siapa namamu?", placeholder="Masukkan nama...")
        submit_name = st.form_submit_button("Join Network 🚀")
        if submit_name and name_input:
            lapor_ke_sheets(name_input)
            st.session_state.user_name = name_input
            st.rerun()
    st.stop()

# --- 6. SIDEBAR & TEMA ---
with st.sidebar:
    st.title(f"👤 {st.session_state.user_name}")
    st.divider()
    theme_choice = st.selectbox("Pilih Vibe Chatbot:", ["Tech (Dark Mode)", "Cyber (Neon)", "Kawaii (Pastel)"])
    
    if st.button("Hapus Riwayat Chat 🗑️"):
        if os.path.exists(MEMORY_FILE):
            os.remove(MEMORY_FILE)
        st.session_state.messages = [
            {"role": "system", "content": "Anda adalah Ahli IT paham coding, sistem, jaringan, komputer yang ahli dan ramah, pakai bahasa Gen z."}
        ]
        st.rerun()
    
    if st.button("Log Out 🔄"):
        st.session_state.user_name = None
        st.rerun()

def apply_style(theme):
    if theme == "Tech (Dark Mode)":
        bg, text, u_bubble, b_bubble = "#0E1117", "#FFFFFF", "#007BFF", "#262730"
        i_user, i_bot = "👤", "💻"
    elif theme == "Cyber (Neon)": 
        bg, text, u_bubble, b_bubble = "#050505", "#00FF41", "linear-gradient(90deg, #FF00FF, #00FFFF)", "#111111"
        i_user, i_bot = "💽 ", "🤖"
    else: 
        bg, text, u_bubble, b_bubble = "#FFF0F5", "#4B0082", "#FFB6C1", "#FFFFFF"
        i_user, i_bot = "🍓", "🧸"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; }}
    .chat-container {{ display: flex; flex-direction: column; margin: 0px 0; }}
    .bubble {{ padding: 12px 18px; border-radius: 18px; max-width: 80%; font-size: 15px; line-height: 1.5; }}
    .user-style {{ align-self: flex-end; background: {u_bubble}; color: white; border-bottom-right-radius: 2px; text-align: right; }}
    .bot-style {{ align-self: flex-start; background-color: {b_bubble}; color: {text}; border: 1px solid #444; border-bottom-left-radius: 2px; }}
    .name-label {{ font-size: 11px; font-weight: bold; margin-bottom: 0px; opacity: 0.7; }}
    </style>
    """, unsafe_allow_html=True)
    return i_user, i_bot

icon_user, icon_bot = apply_style(theme_choice)

# --- 7. TAMPILAN CHAT UTAMA ---
st.title("Digital Agent TKJ")

for message in st.session_state.messages:
    if message["role"] != "system":
        is_user = message["role"] == "user"
        side_class = "user-style" if is_user else "bot-style"
        display_name = st.session_state.user_name if is_user else "GURU TKJ"
        st.markdown(f"""
        <div class="chat-container">
            <div class="name-label" style="text-align: {'right' if is_user else 'left'};">{display_name}</div>
            <div class="bubble {side_class}">{icon_user if is_user else icon_bot} {message['content']}</div>
        </div>
        """, unsafe_allow_html=True)

if prompt := st.chat_input(f"Mau tanya apaa, {st.session_state.user_name}?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Tampilkan chat user langsung
    st.markdown(f"""
    <div class="chat-container">
        <div class="name-label" style="text-align: right;">{st.session_state.user_name}</div>
        <div class="bubble user-style">{icon_user} {prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        save_memory(st.session_state.messages)
        st.rerun()
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
             st.error("🚨 KODE API ERROR: Sepertinya ada masalah dengan key baru. Coba generate ulang lagi.")
        else:
             st.error(f"Error lain: {e}")
