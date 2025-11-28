import pyttsx3
import re

def validate_text(text):
    """
    Task 1.4: Text Input Validation.
    Removes unsupported characters, keeping only alphanumeric and basic punctuation.
    """
    if not text or not isinstance(text, str):
        return False, "Input cannot be empty."
    
    # Regex to keep letters, numbers, and basic punctuation
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,!?\'"]', '', text)
    
    if len(cleaned_text) == 0:
        return False, "No valid characters found."
        
    return True, cleaned_text

def text_to_speech_file(text, filename="output.mp3", rate=200, volume=1.0, voice_idx=0):
    """
    Task 1.1, 1.2, 1.3: Conversion with controls.
    """
    engine = pyttsx3.init()
    
    # Set Rate
    engine.setProperty('rate', rate)
    
    # Set Volume
    engine.setProperty('volume', volume)
    
    # Set Voice (Task 1.2)
    voices = engine.getProperty('voices')
    # Safe index check
    if voice_idx < len(voices):
        engine.setProperty('voice', voices[voice_idx].id)
    
    # Save to file
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename