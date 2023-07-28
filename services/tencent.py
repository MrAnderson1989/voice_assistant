
import base64
import json
import time
from tencentcloud.asr.v20190614 import models as asr_models
from tencentcloud.tts.v20190823 import models as tts_models
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.asr.v20190614 import asr_client
from tencentcloud.tts.v20190823 import tts_client

# Define the TencentASR class
class TencentASR:
    def __init__(self, secret_id, secret_key):
        self.region = config.REGION
        self.secret_id = config.SECRET_ID
        self.secret_key = config.SECRET_KEY
        self.cred = credential.Credential(secret_id, secret_key)
        self.http_profile = HttpProfile()
        self.client_profile = ClientProfile()
        self.client_profile.httpProfile = self.http_profile

    def recognize(self, frames):
        # This method uses the Tencent ASR service to transcribe audio
        # It takes a byte stream of audio frames as input
        # It returns the transcribed text as output

        self.asr_client = asr_client.AsrClient(self.cred, self.region, self.client_profile)
        audio_base64 = base64.b64encode(frames.getvalue()).decode('utf-8')

        req = asr_models.CreateRecTaskRequest()
        params = {
            "EngineModelType": "16k_zh",
            "ChannelNum": 1,
            "ResTextFormat": 0,
            "SourceType": 1,
            "Data": audio_base64,
            "DataLen": len(audio_base64)
        }
        req.from_json_string(json.dumps(params))

        resp = self.asr_client.CreateRecTask(req)
        task_id = json.loads(resp.to_json_string())['Data']['TaskId']

        # Poll for the recognition result
        while True:
            time.sleep(0.5)
            req = asr_models.DescribeTaskStatusRequest()
            params = {"TaskId": task_id}
            req.from_json_string(json.dumps(params))
            resp = self.asr_client.DescribeTaskStatus(req)
            status = json.loads(resp.to_json_string())['Data']['Status']

            if status == 2:  # task completed
                result = json.loads(resp.to_json_string())['Data']['Result']
                return result
            elif status == 3:  # task failed
                raise Exception("Tencent ASR task failed")

    def synthesize(self, text, output_file_path='feedback.mp3'):
        # This method uses the Tencent TTS service to synthesize audio from text
        # It takes a string of text and a file path as input
        # It saves the synthesized audio to the file path
        # It returns the file path

        self.tts_client = tts_client.TtsClient(self.cred, self.region, self.client_profile)
        text_segments = self.split_text(text)
        audio_data_list = []

        for segment in text_segments:
            req = tts_models.TextToVoiceRequest()
            params = {
                "Text": segment,
                "SessionId": "session-123456",
                "ModelType": 1,
                "Volume": 0,
                "Speed": 0,
                "VoiceType": 1004,
                "PrimaryLanguage": 1,
                "SampleRate": 16000,
                "Codec": "mp3",
                "EmotionCategory":"news"
            }
            req.from_json_string(json.dumps(params))

            resp = self.tts_client.TextToVoice(req)
            audio_data_list.append(resp.Audio)

        with open(output_file_path, "wb") as f:
            for base64_audio_data in audio_data_list:
                audio_bytes = base64.b64decode(base64_audio_data)
                f.write(audio_bytes)

        print(f"Audio file saved as {output_file_path}")
        return output_file_path

    @staticmethod
    def split_text(text, max_length=100):
        # This method splits a string of text into segments
        # It takes a string of text and a maximum length as input
        # It returns a list of text segments

        text_segments = []
        while len(text) > max_length:
            segment = text[:max_length]
            text_segments.append(segment)
            text = text[max_length:]
        text_segments.append(text)
        return text_segments

import requests
import hmac
import hashlib
import base64
import time
import json
import config

class FlashRecognizer:
    def __init__(self):
        self.appid = config.APP_ID
        self.secret_id = config.SECRET_ID
        self.secret_key = config.SECRET_KEY

    def _format_sign_string(self, param):
        signstr = "POSTasr.cloud.tencent.com/asr/flash/v1/"
        for t in param:
            if 'appid' in t:
                signstr += str(t[1])
                break
        signstr += "?"
        for x in param:
            tmp = x
            if 'appid' in x:
                continue
            for t in tmp:
                signstr += str(t)
                signstr += "="
            signstr = signstr[:-1]
            signstr += "&"
        signstr = signstr[:-1]
        return signstr

    def _build_header(self):
        header = dict()
        header["Host"] = "asr.cloud.tencent.com"
        return header

    def _sign(self, signstr):
        hmacstr = hmac.new(self.secret_key.encode('utf-8'),
                           signstr.encode('utf-8'), hashlib.sha1).digest()
        s = base64.b64encode(hmacstr)
        s = s.decode('utf-8')
        return s

    def _build_req_with_signature(self, params, header):
        query = sorted(params.items(), key=lambda d: d[0])
        signstr = self._format_sign_string(query)
        signature = self._sign(signstr)
        header["Authorization"] = signature
        requrl = "https://"
        requrl += signstr[4::]
        return requrl

    def _create_query_arr(self):
        query_arr = dict()
        query_arr['appid'] = self.appid
        query_arr['secretid'] = self.secret_id
        query_arr['timestamp'] = str(int(time.time()))
        query_arr['engine_type'] = '16k_zh'
        query_arr['voice_format'] = 'wav'
        query_arr['speaker_diarization'] = 0
        query_arr['hotword_id'] = ''
        query_arr['customization_id'] = ''
        query_arr['filter_dirty'] = 0
        query_arr['filter_modal'] = 0
        query_arr['filter_punc'] = 0
        query_arr['convert_num_mode'] = 1
        query_arr['word_info'] = 0
        query_arr['first_channel_only'] = 1
        query_arr['reinforce_hotword'] = 0
        query_arr['sentence_max_length'] = 0
        return query_arr

    def recognize(self, data):
        header = self._build_header()
        query_arr = self._create_query_arr()
        req_url = self._build_req_with_signature(query_arr, header)
        r = requests.post(req_url, headers=header, data=data)
        return r.text
