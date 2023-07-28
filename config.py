
# Configuration for Tencent ASR and TTS services

# SECRET_ID = "YOUR_SECRET_ID"
# SECRET_KEY = "YOUR_SECRET_KEY"

REGION = "ap-beijing"

# Configuration for GPT-3 API service

# OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
# GPT3_SYSTEM_MESSAGE = "YOUR_CUSTOM_INSTRACTIONS_SYSTEM_MESSAGE"


# Configuration for audio recording

AUDIO_CHUNK = 1024
import pyaudio
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_CHANNELS = 1
AUDIO_RATE = 16000
AUDIO_RECORD_SECONDS = 6

# Configuration for wake word detection

# PORCUPINE_ACCESS_KEY = "YOUR_PORCUPINE_ACCESS_KEY"
# WAKE_WORD = "YOUR_WAKE_WORD"
PORCUPINE_SENSITIVITY = 0.7

