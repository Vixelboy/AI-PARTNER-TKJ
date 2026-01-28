import streamlit as st
from groq import Groq

# --- CONFIG PAGE ---
st.set_page_config(page_title="Guru TKJ AI", page_icon="💻")

# --- FUNCTION UNTUK SUARA ---
def speak(text):
    """Memanggil Google TTS melalui HTML5 Audio"""
    clean_text = text.replace(' ', '%20')
    tts_url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={clean_text}&tl=id&client=tw-ob"
    
    # Komponen HTML untuk memutar audio
    audio_html = f"""
        <audio autoplay>
            <source src="{tts_url}" type="audio/mpeg">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

# --- INITIALIZE GROQ ---
client = Groq(api_key="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")

# --- INITIALIZE SESSION STATE ---
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "greeted" not in st.session_state:
    st.session_state.greeted = False
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah Ahli IT paham coding,sistem,jaringan,komputer yang ahli dan ramah. Gunakan bahasa Gen z."}
    ]

# --- MODAL INPUT NAMA ---
if not st.session_state.user_name:
    st.title("👋 Welcome, Techie!")
    with st.form("name_form"):
        name_input = st.text_input("Masukkan namamu:", placeholder="Contoh: Ikbal")
        submit_name = st.form_submit_button("Join Network")
        
        if submit_name and name_input:
            st.session_state.user_name = name_input
            st.rerun()
    st.stop()

# --- TRIGGER SUARA GREETING OTOMATIS ---
greeting_msg = f"Halo {st.session_state.user_name}, selamat datang di Digital Agent T K J."
if not st.session_state.greeted:
    speak(greeting_msg)
    st.session_state.greeted = True
    st.toast(f"🔊 Mengucapkan salam...")

# --- SIDEBAR: TEMA & TOMBOL SUARA MANUAL ---
with st.sidebar:
    st.title(f"👤 {st.session_state.user_name}")
    
    # TOMBOL MANUAL (Plan B)
    if st.button("🔊 Putar Ulang Salam"):
        speak(greeting_msg)
        
    st.divider()
    theme_choice = st.selectbox("Pilih Vibe:", ["Tech (Dark Mode)", "Cyberpunk (Neon)", "Kawaii (Pastel)"])
    
    if st.button("Reset Session 🔄"):
        st.session_state.user_name = None
        st.session_state.greeted = False
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# --- CSS INJECTION ---
def apply_style(theme):
    if theme == "Tech (Dark Mode)":
        bg, text, u_bubble, b_bubble = "#0E1117", "#FFFFFF", "#007BFF", "#262730"
        i_user, i_bot = "👤", "💻"
    elif theme == "Cyberpunk (Neon)":
        bg, text, u_bubble, b_bubble = "#050505", "#00FF41", "linear-gradient(90deg, #FF00FF, #00FFFF)", "#111111"
        i_user, i_bot = "🕶️", "🤖"
    else: # Kawaii
        bg, text, u_bubble, b_bubble = "#FFF0F5", "#4B0082", "#FFB6C1", "#FFFFFF"
        i_user, i_bot = "🍓", "🧸"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; }}
    .chat-container {{ display: flex; flex-direction: column; margin: 10px 0; }}
    .bubble {{ padding: 12px 18px; border-radius: 18px; max-width: 80%; font-size: 15px; }}
    .user-style {{ align-self: flex-end; background: {u_bubble}; color: white; border-bottom-right-radius: 2px; text-align: right; }}
    .bot-style {{ align-self: flex-start; background-color: {b_bubble}; color: {text}; border: 1px solid #444; border-bottom-left-radius: 2px; }}
    .name-label {{ font-size: 11px; font-weight: bold; margin-bottom: 2px; opacity: 0.8; }}
    </style>
    """, unsafe_allow_html=True)
    return i_user, i_bot

icon_user, icon_bot = apply_style(theme_choice)

# --- RENDER CHAT ---
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

# --- INPUT LOGIC ---
if prompt := st.chat_input(f"Ping me something, {st.session_state.user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        response = client.chat.completions.create(model="llama-3.1-8b-instant", messages=st.session_state.messages)
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
    except Exception as e:
        st.error(f"Koneksi RTO: {e}")
