import os
from pathlib import Path
from groq import Groq

def call_sst(file_path: str) -> str:
    """
    Transcribe an audio file using the Groq Whisper API via the Groq Python client.

    Args:
    file_path (str): Path to the audio file to be transcribed.

    Returns:
    str: The transcribed text.

    Raises:
    Exception: If there's an error in the API call or file handling.
    """
    # Ensure the file exists
    print('file_path ----->',file_path)
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    # Get the API key from environment variable
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    # Initialize the Groq client
    client = Groq(api_key=api_key)

    try:
        # Open the audio file
        with open(file_path, "rb") as audio_file:
            # Make the API call
            response = client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio_file
            )

        # Return the transcribed text
        print('response.text ----->',response.text)
        return response.text

    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")
