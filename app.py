import streamlit as st
from groq import Groq

# Konfigurasi Halaman
st.set_page_config(page_title="Guru TKJ AI", page_icon="💻")
st.title("🤖 Kelas Digital Pak Guru TKJ")
st.caption("Materi: Jaringan, Mikrotik, Cybersecurity, & Coding")

# Inisialisasi Client Groq dengan API Key Anda
client = Groq(api_key="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")

# Inisialisasi riwayat chat agar tidak hilang saat refresh
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Anda adalah Pak Guru TKJ yang ahli dan ramah. Gunakan analogi jaringan dalam menjelaskan."}
    ]

# Menampilkan riwayat chat di layar
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input dari Siswa
if prompt := st.chat_input("Tanya apa hari ini, Nak?"):
    # Tampilkan pesan siswa
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Kirim ke Groq
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages
        )
        
        answer = response.choices[0].message.content
        
        # Tampilkan respon guru
        with st.chat_message("assistant"):
            st.markdown(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.error(f"Waduh, koneksi putus: {e}")