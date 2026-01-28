import streamlit as st
import os
import json

# --- FUNGSI TAMBAHAN UNTUK SIDEBAR ---
def start_new_chat():
    st.session_state.messages = [
        {"role": "system", "content": "Anda ahli IT ramah, gunakan bahasa Gen Z dan analogi jaringan."}
    ]
    # Kita beri nama file baru berdasarkan timestamp agar riwayat lama tidak tertimpa
    new_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.current_chat_file = f"chat_{new_id}.json"
    st.rerun()

# --- CSS FULL SCREEN & SIDEBAR CUSTOM ---
def apply_full_3d_style():
    st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .main .block-container { padding-top: 1rem; max-width: 95%; }
    
    /* Background Full Screen */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Tombol Baru ala Gemini */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: 0.3s;
        text-align: left;
        padding: 10px;
    }
    .stButton>button:hover {
        background: rgba(0, 210, 255, 0.2);
        border-color: #00d2ff;
    }

    /* Chat Bubbles */
    .bubble {
        padding: 15px 25px;
        border-radius: 20px;
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        margin-bottom: 10px;
    }
    .user-3d { align-self: flex-end; background: rgba(0, 150, 255, 0.2); border-right: 5px solid #00d2ff; }
    .bot-3d { align-self: flex-start; background: rgba(255, 255, 255, 0.03); border-left: 5px solid #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

# --- MAIN APP INTERFACE ---
st.set_page_config(page_title="Vixel Chat AI", page_icon="🤖", layout="wide")
apply_full_3d_style()

# --- SIDEBAR ALA GEMINI ---
with st.sidebar:
    st.markdown(f"### 🚀 VixelBoy AI")
    st.caption(f"Connected as: {st.session_state.user_name}")
    
    # 1. Tombol Chat Baru
    if st.button("➕ Chat Baru"):
        st.session_state.messages = [{"role": "system", "content": "Anda ahli IT ramah, gunakan bahasa Gen Z dan analogi jaringan."}]
        st.rerun()

    st.write("---")
    
    # 2. Riwayat Chat (Daftar File JSON di folder)
    st.markdown("🕒 **Riwayat Chat**")
    all_files = [f for f in os.listdir() if f.endswith('.json') and f.startswith('chat_')]
    for file in sorted(all_files, reverse=True)[:5]: # Tampilkan 5 terakhir
        if st.button(f"📄 {file[:15]}...", key=file):
            st.session_state.messages = load_memory_from_file(file)
            st.rerun()

    st.write("---")

    # 3. Opsi Tema & Settings
    st.markdown("⚙️ **Settings**")
    theme_choice = st.selectbox("Ganti Tema:", ["Cyberpunk Neon", "Space Dark", "Kawaii Pink"])
    
    if st.button("🗑️ Hapus Semua Chat"):
        # Logika hapus semua file JSON riwayat
        for f in all_files: os.remove(f)
        st.session_state.messages = [{"role": "system", "content": "..."}]
        st.rerun()

    if st.button("🔄 Log Out"):
        st.session_state.user_name = None
        st.rerun()

# --- RENDER CHAT UTAMA ---
st.markdown("<h2 style='text-align: center; color: white;'>Digital Agent TKJ</h2>", unsafe_allow_html=True)

# Container khusus untuk menampung chat agar bisa di-scroll
chat_placeholder = st.container()

with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            is_user = msg["role"] == "user"
            style = "user-3d" if is_user else "bot-3d"
            label = st.session_state.user_name if is_user else "SERVER AI"
            
            st.markdown(f"""
            <div style="display: flex; flex-direction: column;">
                <div class="{style} bubble">
                    <small style="color: cyan;">{label}</small><br>
                    {msg['content']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- INPUT COMMAND ---
if prompt := st.chat_input("Tanyakan sesuatu ke Digital Agent..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # ... (Logika Groq dan Save Memory tetap sama)
    st.rerun()
