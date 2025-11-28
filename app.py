import streamlit as st
from gtts import gTTS  # Changed from pyttsx3 to gTTS
import os
import time
import PyPDF2
from src.ai_module import get_mistral_response

# --- 1. Page & CSS Configuration ---
st.set_page_config(page_title="SpeakSense AI", layout="wide", page_icon="🎙️")

# Custom CSS for WhatsApp-style Chat
st.markdown("""
<style>
    .stApp { background-color: #ECE5DD; }
    .user-bubble {
        background-color: #DCF8C6; color: black; padding: 10px 15px;
        border-radius: 10px 0px 10px 10px; margin: 10px 0 10px auto;
        width: fit-content; max-width: 75%; text-align: left;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1); font-family: sans-serif;
    }
    .bot-bubble {
        background-color: #FFFFFF; color: black; padding: 10px 15px;
        border-radius: 0px 10px 10px 10px; margin: 10px 0 10px 0;
        width: fit-content; max-width: 75%; text-align: left;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1); font-family: sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎙️ DocuVoice AI")

# --- 2. Helper Functions ---

def extract_text_from_file(uploaded_file):
    text = ""
    try:
        if uploaded_file.type == "text/plain":
            text = str(uploaded_file.read(), "utf-8")
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        return f"Error reading file: {e}"
    return text

def text_to_audio_file(text, lang_code, slow_mode, filename):
    """Generates audio file using gTTS (Cloud Compatible)."""
    try:
        # gTTS connects to Google API, works on Linux/Cloud
        tts = gTTS(text=text, lang=lang_code, tld=get_tld(lang_code), slow=slow_mode)
        tts.save(filename)
        return True
    except Exception as e:
        st.error(f"TTS Generation Error: {e}")
        return False

def get_tld(lang_code):
    """Helper to get accent domain (Top Level Domain)"""
    # Maps language code to Google domain for accents
    if lang_code == 'en-us': return 'com'
    if lang_code == 'en-uk': return 'co.uk'
    if lang_code == 'en-in': return 'co.in'
    if lang_code == 'en-au': return 'com.au'
    return 'com'

# --- 3. Sidebar & Settings ---
st.sidebar.header("⚙️ Configuration")
api_key = "TmwqQXMqrJHMjInxDV7DYxq1lR4hIMSY"

# Cloud-Friendly Voice Options (Accents)
voice_options = {
    "English (US)": "en-us",
    "English (UK)": "en-uk",
    "English (India)": "en-in",
    "English (Australia)": "en-au",
    "French": "fr",
    "Spanish": "es"
}

# --- 4. Main Tabs ---
tab1, tab2 = st.tabs(["🗣️ Smart TTS Converter", "💬 AI Chat (WhatsApp Style)"])

# ==========================================
# TAB 1: Text-to-Speech
# ==========================================
with tab1:
    st.header("Document & Text to Speech")

    input_method = st.radio("Input Source:", ["Type Text", "Upload File (PDF/TXT)"], horizontal=True)

    tts_text = ""
    if input_method == "Type Text":
        tts_text = st.text_area("Enter text:", height=150)
    else:
        uploaded_file = st.file_uploader("Upload document", type=["txt", "pdf"])
        if uploaded_file:
            with st.spinner("Processing file..."):
                tts_text = extract_text_from_file(uploaded_file)
                st.success(f"Loaded {len(tts_text)} characters.")
                with st.expander("Preview Text"):
                    st.text(tts_text[:500] + "...")

    # Controls
    c1, c2 = st.columns(2)
    with c1:
        selected_accent_label = st.selectbox("Select Accent/Language", list(voice_options.keys()))
        selected_lang_code = voice_options[selected_accent_label]
    with c2:
        speed_label = st.selectbox("Speaking Speed", ["Normal", "Slow"])
        is_slow = (speed_label == "Slow")

    if st.button("Generate Audio 🎧"):
        if tts_text.strip():
            timestamp = int(time.time())
            output_filename = f"output_{timestamp}.mp3"
            
            with st.spinner("Generating audio..."):
                success = text_to_audio_file(tts_text, selected_lang_code, is_slow, output_filename)
            
            if success:
                st.audio(output_filename, format="audio/mp3")
                with open(output_filename, "rb") as f:
                    st.download_button("📥 Download MP3", f, file_name="speech.mp3", mime="audio/mp3")
        else:
            st.warning("Please input some text first.")

# ==========================================
# TAB 2: Chat
# ==========================================
with tab2:
    st.header("Mistral AI Chat")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)
                if st.button("🔊", key=f"listen_{i}", help="Listen"):
                    chat_file = f"chat_{i}.mp3"
                    # Use US English normal speed for chat
                    if text_to_audio_file(message["content"], "en-us", False, chat_file):
                        st.audio(chat_file, format="audio/mp3", start_time=0)

    if prompt := st.chat_input("Type a message..."):
        if not api_key:
            st.error("Please enter API Key in sidebar.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": "..."})
            st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["content"] == "...":
        with st.spinner("Mistral is typing..."):
            user_prompt = st.session_state.messages[-2]["content"]
            response_text = get_mistral_response(user_prompt, api_key)
            st.session_state.messages[-1]["content"] = response_text
            st.rerun()

