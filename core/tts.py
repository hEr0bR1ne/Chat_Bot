import os
import asyncio
import edge_tts

class TextToSpeech:
    def __init__(self):
        pass

    def text_to_speech(self, text, voice, callback=None):
        """文字转语音，完成后调用callback"""
        async def _tts():
            try:
                communicate = edge_tts.Communicate(
                    text,
                    voice
                )
                await communicate.save("output.wav")
                os.system("afplay output.wav")
                if callback:
                    callback(success=True)
            except Exception as e:
                if callback:
                    callback(success=False, error=str(e))
        asyncio.run(_tts()) 