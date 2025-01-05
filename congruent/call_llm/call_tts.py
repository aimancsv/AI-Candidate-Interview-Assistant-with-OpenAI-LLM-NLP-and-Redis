import os
from typing import AsyncIterable
from congruent.call_llm.call_llm import call_llm_groq_stream
from elevenlabs.client import ElevenLabs

from fastapi.responses import StreamingResponse
import io

eleven_labs_api_key = os.getenv("ELEVEN_LABS_API_KEY")
client_elevenlabs = ElevenLabs(api_key=eleven_labs_api_key)

async def call_tts_stream(text_stream: AsyncIterable[str]):
    try:
        audio_stream = client_elevenlabs.generate(
            text=text_stream,
            voice="Matilda",
            model="eleven_turbo_v2",
            stream=True
        )

        for chunk in audio_stream:
            yield chunk
    except Exception as e:
        print(f"Speech generation failed: {str(e)}")
        yield b''


async def generate_audio_stream(prompt, user_query, session_id):
    try:
        audio_stream = client_elevenlabs.generate(
            text=call_llm_groq_stream(prompt, user_query, session_id),
            voice="Matilda",
            model="eleven_turbo_v2",
            stream=True,
        )

        for chunk in audio_stream:
            yield chunk
    except Exception as e:
        print(f"Speech generation failed: {str(e)}")
        yield b''
