# 🎙️ SpeakSense AI: Cloud-Native Chat & TTS

## 📌 Overview

**SpeakSense AI** is a robust technical assignment submission that integrates **Cloud-Based Text-to-Speech (TTS)** and **Generative AI (Mistral API)** into a unified web application.

Designed for seamless deployment on **Streamlit Cloud**, this application features a "WhatsApp-style" chat interface, PDF document reading, and multi-accent speech synthesis without requiring local system audio drivers.

## 🚀 Key Features

### 1. Cloud-Compatible TTS Engine

* **Universal Deployment:** Uses `gTTS` (Google TTS) to ensure the app works on any device or cloud server (Streamlit Cloud, Docker, Linux) without crashing.
* **Document Reader:** Upload **PDF or TXT files** and convert them to audio instantly.
* **Global Accents:** Supports multiple English accents (US, UK, India, Australia) plus French and Spanish.
* **Download Support:** Users can download the generated speech as an **MP3 file** for offline listening.

### 2. Intelligent Chat Interface

* **Mistral AI Integration:** Connects to the Mistral API for high-quality, real-time conversational AI.
* **WhatsApp-Style UI:** Custom CSS styling provides a familiar, polished messaging experience (Green/White bubbles).
* **Chat-to-Speech:** Includes a **"Listen" button** next to every AI response, allowing users to hear the answer immediately.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python) with Custom CSS
* **AI Model:** Mistral AI API (`mistral-tiny`)
* **TTS Engine:** `gTTS` (Google Text-to-Speech - Online & Cloud Ready)
* **File Processing:** `PyPDF2`
* **HTTP Requests:** `requests`

---

## 📂 Project Structure

```text
/Speaksense_AI
│
├── app.py                 # Main Application (UI & Logic)
├── requirements.txt       # Project Dependencies (Crucial for Cloud Deployment)
├── README.md              # Documentation
│
└── /src
    └── ai_module.py       # API connection logic
```

---

## ⚙️ Installation & Setup

### Option A: Run Locally

1. **Clone the repository.**
2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
3. **Run the App:**

   ```bash
   streamlit run app.py
   ```

### Option B: Deploy to Streamlit Cloud (Recommended)

1. Push this code to a GitHub repository.
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/).
3. Connect your GitHub account and select this repository.
4. **Important:** Ensure `requirements.txt` is in the root folder.
5. Click **Deploy**.

---

## 📖 User Guide

### Tab 1: Smart TTS Converter

1. **Select Input:** Choose "Type Text" or "Upload File".
2. **Upload:** Drop a PDF or TXT file to extract text automatically.
3. **Customize:** Select your preferred **Accent/Language** (e.g., English UK, English India) and **Speed**.
4. **Generate:** Click "Generate Audio".
5. **Download:** Save the result using the "Download MP3" button.

### Tab 2: AI Chat

1. **API Key:** Enter your Mistral API Key in the **Sidebar**.
2. **Chat:** Type your message in the input bar (WhatsApp-style interface).
3. **Listen:** Click the 🔊 speaker icon next to any AI response to hear it spoken aloud.

---

## 🛡️ Robustness & Error Handling

* **Cloud Stability:** Replaced `pyttsx3` with `gTTS` to eliminate "ModulenotFound" and audio driver errors on Linux servers.
* **API Timeouts:** Handles Mistral API connection drops gracefully.
* **Input Validation:** Prevents processing of empty text or corrupt files.

---

## 👨‍💻 Author

* **Name:** Janavi Singh

