import streamlit as st
from groq import Groq

# --- CONFIG PAGE ---
st.set_page_config(page_title="Guru TKJ AI", page_icon="💻")

# --- INITIALIZE GROQ ---
# Catatan: Simpan API Key di st.secrets untuk keamanan jika dideploy
client = Groq(api_key="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")

# --- SIDEBAR: TEMA ---
with st.sidebar:
    st.title("⚙️ Interface Settings")
    theme_choice = st.selectbox(
        "Pilih Vibe Chatbot:",
        ["Tech (Dark Mode)", "Cyberpunk (Neon)", "Kawaii (Pastel)"]
    )
    if st.button("Clear Chat 🗑️"):
        st.session_state.messages = [
            {"role": "system", "content": "Anda adalah Ahli IT paham coding,sistem,jaringan,komputer yang ahli dan ramah. Gunakan analogi jaringan dalam menjelaskan,dan pakai bahasa Gen z"}
        ]
        st.rerun()

# --- CSS INJECTION & THEME LOGIC ---
def apply_style(theme):
    if theme == "Tech (Dark Mode)":
        bg, text, u_bubble, b_bubble, font = "#0E1117", "#FFFFFF", "#007BFF", "#262730", "sans-serif"
        i_user, i_bot = "👤", "💻"
    elif theme == "Cyberpunk (Neon)":
        bg, text, u_bubble, b_bubble, font = "#050505", "#00FF41", "linear-gradient(90deg, #FF00FF, #00FFFF)", "#111111", "'Courier New', monospace"
        i_user, i_bot = "🕶️", "🤖"
    else: # Kawaii
        bg, text, u_bubble, b_bubble, font = "#FFF0F5", "#4B0082", "#FFB6C1", "#FFFFFF", "'Comic Sans MS', cursive"
        i_user, i_bot = "🍓", "🧸"

    st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {text}; font-family: {font}; }}
    .chat-container {{ display: flex; flex-direction: column; margin: 10px 0; }}
    .bubble {{
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 80%;
        margin-bottom: 5px;
        font-size: 15px;
        line-height: 1.4;
    }}
    .user-style {{
        align-self: flex-end;
        background: {u_bubble};
        color: white;
        border-bottom-right-radius: 2px;
        text-align: right;
    }}
    .bot-style {{
        align-self: flex-start;
        background-color: {b_bubble};
        color: {text};
        border: 1px solid #444;
        border-bottom-left-radius: 2px;
    }}
    </style>
    """, unsafe_allow_html=True)
    return i_user, i_bot

icon_user, icon_bot = apply_style(theme_choice)

# --- HEADER ---
st.title("Digital Agent TKJ")
st.caption(f"Vibe saat ini: {theme_choice} | Skill: Networking, Cybersec, Coding")

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah Ahli IT paham coding,sistem,jaringan,komputer yang ahli dan ramah. Gunakan analogi jaringan dalam menjelaskan,dan pakai bahasa Gen z"}
    ]

# --- RENDER CHAT ---
for message in st.session_state.messages:
    if message["role"] != "system":
        side_class = "user-style" if message["role"] == "user" else "bot-style"
        icon = icon_user if message["role"] == "user" else icon_bot
        st.markdown(f"""
        <div class="chat-container">
            <div class="bubble {side_class}">
                {icon} <b>{message['role'].upper()}</b><br>{message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- INPUT LOGIC ---
if prompt := st.chat_input("Ping me something..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun() # Refresh untuk nampilin bubble baru
        
    except Exception as e:
        st.error(f"Koneksi RTO (Request Time Out) nih: {e}")
