
import os
import logging
import pyaudio
import config
from hardware.microphone import AudioRecorder, WakeWordDetector
from services.tencent import TencentASR
from services.gpt3 import GPT
from helpers.helper import play_audio



# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Jarvis:
    def __init__(self):
        self.wake_word = config.WAKE_WORD
        self.audio_recorder = AudioRecorder()
        self.wake_word_detector = WakeWordDetector()
        self.tencent_asr = TencentASR(config.SECRET_ID,config.SECRET_KEY)
        self.chat_gpt = GPT()

    # Function to provide feedback when wake word is detected
    def wake_word_feedback(self):
        feedback_text = "您好，有什么可以帮您？"
        if os.path.exists('feedback.mp3'):
            play_audio('feedback.mp3')
        else:    
            audio_file_path = self.tencent_asr.synthesize(feedback_text)
            play_audio(audio_file_path)

    # Function to handle the actions after wake word is detected
    def callback(self, audio_stream, pa):
        self.wake_word_feedback()
        
        frames = self.audio_recorder.record_audio(audio_stream)

        question_text = self.tencent_asr.recognize(frames)

        print('question_text:'+question_text)

        response = self.chat_gpt.generate_response(question_text)

        print('response:'+response)

        audio_file_path =  self.tencent_asr.synthesize(response,'answer.mp3')

        play_audio(audio_file_path)

    def run(self):
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=self.wake_word_detector.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.wake_word_detector.porcupine.frame_length,
            input_device_index=None)

        self.wake_word_detector.listen_for_wake_word(audio_stream=audio_stream, pa=pa,callback=self.callback)

if __name__ == "__main__":
    jarvis = Jarvis()
    jarvis.run()
