def apply_3d_style():
    st.markdown("""
    <style>
    /* 1. Menghilangkan padding default Streamlit agar header/footer rata */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem; /* Memberi ruang agar chat input tidak tertutup */
        max-width: 95%;
    }

    /* 2. Menghilangkan header default Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 3. Background Utama */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        background-attachment: fixed;
    }

    /* 4. Membuat Top Bar (Hitam Rata Atas) */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0.8) !important;
        backdrop-filter: blur(10px);
        height: 50px;
    }

    /* 5. Custom Styling untuk Chat Input (Area Hitam Bawah) */
    .stChatInputContainer {
        padding: 1.5rem;
        background-color: rgba(0, 0, 0, 0.5) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        bottom: 0px;
    }

    /* --- Styling Bubble (Tetap sesuai kode Anda) --- */
    .chat-wrapper {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 10px;
    }

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

    .user-3d {
        align-self: flex-end;
        background: rgba(0, 123, 255, 0.25);
        border-right: 4px solid #00d2ff;
    }

    .bot-3d {
        align-self: flex-start;
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ff00ff;
    }
    </style>
    """, unsafe_allow_html=True)
