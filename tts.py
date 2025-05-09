from google.cloud import texttospeech
from google.cloud.texttospeech import StreamingAudioConfig
from config import tts_client

def synthesize_streaming(text_iterator):
    streaming_config = texttospeech.StreamingSynthesizeConfig(
        voice=texttospeech.VoiceSelectionParams(
            name="ko-KR-Chirp3-HD-Zephyr",
            language_code="ko-KR"
        ),
        streaming_audio_config=StreamingAudioConfig(
            audio_encoding=texttospeech.AudioEncoding.PCM,
            sample_rate_hertz=24000,
        )
    )

    config_request = texttospeech.StreamingSynthesizeRequest(
        streaming_config=streaming_config
    )

    def request_generator():
        yield config_request
        for text in text_iterator:
            yield texttospeech.StreamingSynthesizeRequest(
                input=texttospeech.StreamingSynthesisInput(text=text)
            )

    streaming_responses = tts_client.streaming_synthesize(request_generator())

    for response in streaming_responses:
        yield response.audio_content