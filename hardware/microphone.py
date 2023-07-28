
import io
import pyaudio
import wave
import config

class AudioRecorder:
    def __init__(self):
        self.chunk = config.AUDIO_CHUNK
        self.format = config.AUDIO_FORMAT
        self.channels = config.AUDIO_CHANNELS
        self.rate = config.AUDIO_RATE
        self.record_seconds = config.AUDIO_RECORD_SECONDS
        self.pyaudio_instance = pyaudio.PyAudio()

    def record_audio(self, audio_stream):
        # Record audio from the audio stream and return a byte stream
        frames = []

        for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
            data = audio_stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

        # Convert the audio data to bytes
        audio_stream = b''.join(frames)

        audio_file = io.BytesIO()
        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio_instance.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(audio_stream)
        wf.close()

        return audio_file



import pyaudio
import pvporcupine
import struct
import config

class WakeWordDetector:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=config.PORCUPINE_ACCESS_KEY,
            keywords=[config.WAKE_WORD],
            sensitivities=[config.PORCUPINE_SENSITIVITY]
        )

    def get_next_audio_frame(self, audio_stream):
        # Get the next audio frame from the audio stream
        pcm = audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
        return pcm

    def listen_for_wake_word(self, audio_stream, pa,callback):
        # Listen for the wake word in the audio stream and call the callback function
        try:
            print("Listening...")

            while True:
                pcm = self.get_next_audio_frame(audio_stream)
                keyword_index = self.porcupine.process(pcm)
                if keyword_index >= 0:
                    print("Wake word detected!")
                    callback(audio_stream,pa)
                    continue

        finally:
            if audio_stream is not None:
                audio_stream.close()

            if self.porcupine is not None:
                self.porcupine.delete()
