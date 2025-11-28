import streamlit as st
import pyttsx3
import os
import time
import PyPDF2
from src.ai_module import get_mistral_response

# --- 1. Page & CSS Configuration ---
st.set_page_config(page_title="VocalForge Suite", layout="wide", page_icon="🤖")

# Custom CSS for WhatsApp-style Chat
st.markdown("""
<style>
    /* Main Background */
    .stApp { background-color: #FFFFF; }
    
    /* User Message (Green, Right) */
    .user-bubble {
        background-color: #FFFFFF;
        color: black;
        padding: 10px 15px;
        border-radius: 10px 0px 10px 10px;
        margin: 10px 0 10px auto;
        width: fit-content;
        max-width: 75%;
        text-align: left;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        font-family: sans-serif;
    }

    /* Bot Message (White, Left) */
    .bot-bubble {
        background-color: #FFFFFF;
        color: black;
        padding: 10px 15px;
        border-radius: 0px 10px 10px 10px;
        margin: 10px 0 10px 0;
        width: fit-content;
        max-width: 75%;
        text-align: left;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        font-family: sans-serif;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 VocalForge Suite")

# --- 2. Helper Functions ---

def extract_text_from_file(uploaded_file):
    """Extracts text from PDF or TXT files."""
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

def text_to_audio_file(text, voice_id, rate, filename):
    """Generates audio file using pyttsx3."""
    # Initialize engine specifically for this run to avoid thread conflicts
    engine = pyttsx3.init()
    if voice_id:
        engine.setProperty('voice', voice_id)
    engine.setProperty('rate', rate)
    engine.save_to_file(text, filename)
    engine.runAndWait()

# --- 3. Sidebar & Settings ---
st.sidebar.header("⚙️ Configuration")
api_key = "TmwqQXMqrJHMjInxDV7DYxq1lR4hIMSY"

# Load System Voices
try:
    engine_init = pyttsx3.init()
    voices = engine_init.getProperty('voices')
    voice_map = {}
    for v in voices:
        label = v.name
        if "David" in label or "Mark" in label: label += " (Male ♂️)"
        elif "Zira" in label or "Eva" in label: label += " (Female ♀️)"
        voice_map[label] = v.id
except Exception as e:
    st.sidebar.error("⚠️ Voice drivers not found. Run `pip install pypiwin32`.")
    voice_map = {"Default": None}

# --- 4. Main Tabs ---
tab1, tab2 = st.tabs(["🗣️ Smart TTS Converter", "💬 AI Chat (WhatsApp Style)"])

# ==========================================
# TAB 1: Text-to-Speech (Pro Features)
# ==========================================
with tab1:
    st.header("Document & Text to Speech")

    # Input Method
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
        selected_label = st.selectbox("Select Voice", list(voice_map.keys()))
        selected_voice_id = voice_map[selected_label]
    with c2:
        tone_label = st.selectbox("Select Tone", ["Serious (Slow)", "Normal", "Excited (Fast)"])
        rate_map = {"Serious (Slow)": 125, "Normal": 175, "Excited (Fast)": 225}
        selected_rate = rate_map[tone_label]

    # Generate Action
    if st.button("Generate Audio 🎧"):
        if tts_text.strip():
            try:
                timestamp = int(time.time())
                output_filename = f"output_{timestamp}.mp3"
                
                with st.spinner("Generating audio..."):
                    text_to_audio_file(tts_text, selected_voice_id, selected_rate, output_filename)
                
                st.audio(output_filename, format="audio/mp3")
                
                # Download Button
                with open(output_filename, "rb") as f:
                    st.download_button("📥 Download MP3", f, file_name="speech.mp3", mime="audio/mp3")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please input some text first.")

# ==========================================
# TAB 2: Chat (WhatsApp Style)
# ==========================================
with tab2:
    st.header("Mistral AI Chat")

    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Render Chat History ---
    chat_container = st.container()
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bot-bubble">{message["content"]}</div>', unsafe_allow_html=True)
                # Listen Button
                if st.button("🔊", key=f"listen_{i}", help="Listen to this response"):
                    try:
                        chat_file = f"chat_{i}.mp3"
                        # Use default voice for speed
                        text_to_audio_file(message["content"], list(voice_map.values())[0], 175, chat_file)
                        st.audio(chat_file, format="audio/mp3", start_time=0)
                    except:
                        st.warning("Could not play audio.")

    # --- Input Area ---
    if prompt := st.chat_input("Type a message..."):
        if not api_key:
            st.error("Please enter API Key in sidebar.")
        else:
            # Add User Message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Add Placeholder for Assistant
            st.session_state.messages.append({"role": "assistant", "content": "..."})
            
            # Force Rerun to show User message immediately
            st.rerun()

    # --- Processing Response (After Rerun) ---
    # Check if the last message is a placeholder "..."
    if st.session_state.messages and st.session_state.messages[-1]["content"] == "...":
        with st.spinner("Mistral is typing..."):
            # Get real user prompt (second to last message)
            user_prompt = st.session_state.messages[-2]["content"]
            response_text = get_mistral_response(user_prompt, api_key)
            
            # Update the placeholder with real response
            st.session_state.messages[-1]["content"] = response_text
            st.rerun()