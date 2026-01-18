import streamlit as st
from groq import Groq

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Guru TKJ AI", page_icon="💻")
st.title("🤖 Kelas Digital Pak Guru TKJ")
st.caption("Materi: Jaringan, Mikrotik, Cybersecurity, Coding, dll")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah Pak Guru TKJ yang ahli dan ramah. Gunakan bahasa SMK dan analogi jaringan."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Tanya apa hari ini, Nak?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        answer = response.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Waduh, koneksi putus: {e}")
