import asyncio
import os
import wave
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import List, Dict, TypedDict

# Define a type for the music request object
class MusicRequest(TypedDict):
    instrument: str
    genre: str
    mood: str


load_dotenv()
my_apikey = os.getenv("API_KEY")

if not my_apikey:
    raise ValueError("API_KEY environment variable not set. Please set it in your .env file.")

client = genai.Client(api_key=my_apikey, http_options={'api_version': 'v1alpha'})


async def generate_music(requests: List[MusicRequest], duration: int = 60, filename: str = "generated_music.wav"):
    """Generates music based on a list of requests and saves it to a WAV file.

    Args:
        requests: A list of MusicRequest objects, each containing
                  'instrument', 'genre', and 'mood'.
        duration: The duration of the music generation in seconds.
        filename: The name of the file to save the generated music to.
    """

    async def receive_audio(session):
        """Background task to process and save incoming audio to a WAV file."""
        try:
            with wave.open(filename, "wb") as wf:  # Open a WAV file for writing
                wf.setnchannels(2)  # Stereo audio
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(48000)  # Sample rate (adjust if needed)

                while True:
                    async for message in session.receive():
                        print(f"Received message: {message}")  # Print the entire message
                        if message.server_content and message.server_content.audio_chunks:
                            audio_data = message.server_content.audio_chunks[0].data
                            print(f"Received audio chunk of size: {len(audio_data)}")
                            wf.writeframes(audio_data)  # Write audio data to the file
                        else:
                            print("Received a message without audio content.")
                        await asyncio.sleep(10 ** -12)
        except Exception as e:
            print(f"Error in receive_audio: {e}")

    async with (
        client.aio.live.music.connect(model='models/lyria-realtime-exp') as session,
        asyncio.TaskGroup() as tg,
    ):
        print("Connected to the music generation service.")
        receive_task = tg.create_task(receive_audio(session))

        # Combine requests into prompts with decreasing weights
        num_requests = len(requests)
        prompts = [
            types.WeightedPrompt(
                text=f"Happy Dance {req['instrument']} {req['genre']} {req['mood']}",
                weight=1.0 - (i / num_requests)  # Decrease weight for each prompt
            )
            for i, req in enumerate(requests)
        ]
        await session.set_weighted_prompts(prompts=prompts)

        # You might want to make BPM and temperature configurable as well.
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(bpm=90, temperature=0.7)
        )

        print("Starting music generation...")
        await session.play()
        print(f"Music generation started. Check for audio output in {filename}.  Running for {duration} seconds.")

        try:
            await asyncio.sleep(duration)  # Run for the specified duration
        except asyncio.CancelledError:
            pass
        finally:
            print("Music generation stopped.")
            if 'receive_task' in locals() and not receive_task.done():
                receive_task.cancel()  # Cancel the receive_audio task
            await session.stop()  # Stop the music generation session



async def main():
    # Example usage:
    music_requests: List[MusicRequest] = [
        {"instrument": "Bongos", "genre": "Acid Jazz", "mood": "Acoustic Instruments"},
        {"instrument": "Ragtime Piano", "genre": "Post-Punk", "mood": "Emotional"},
        {"instrument": "Viola Ensemble", "genre": "60s Psychedelic Rock", "mood": "Dreamy"},  # Added a third request
    ]
    await generate_music(music_requests, duration=10, filename="my_music.wav")


if __name__ == "__main__":
    asyncio.run(main())