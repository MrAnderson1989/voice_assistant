
import sys
sys.path.append("../hardware")

from hardware.microphone import AudioRecorder, WakeWordDetector

def test_audio_recorder():
    audio_recorder = AudioRecorder()
    assert audio_recorder is not None

def test_wake_word_detector():
    wake_word_detector = WakeWordDetector()
    assert wake_word_detector is not None
