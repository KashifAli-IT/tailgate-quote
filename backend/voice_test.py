import asyncio
import base64
import json
import os
import queue

import sounddevice as sd
import websockets
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
WS_URL = "wss://agents.assemblyai.com/v1/ws"

SAMPLE_RATE = 24_000
CHANNELS = 1
BLOCK_SIZE = 2_400

speaker_buffer = queue.Queue()


async def send_microphone(websocket):
    loop = asyncio.get_running_loop()
    microphone_queue = asyncio.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print("Microphone:", status)

        audio_data = bytes(indata)

        loop.call_soon_threadsafe(
            microphone_queue.put_nowait,
            audio_data,
        )

    print("🎤 Microphone started.")
    print("Speak normally. Press Ctrl+C to stop.\n")

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=CHANNELS,
        dtype="int16",
        callback=audio_callback,
    ):
        while True:
            audio_data = await microphone_queue.get()

            await websocket.send(
                json.dumps(
                    {
                        "type": "input.audio",
                        "audio": base64.b64encode(
                            audio_data
                        ).decode("ascii"),
                    }
                )
            )


async def receive_messages(websocket):
    while True:
        raw_message = await websocket.recv()
        event = json.loads(raw_message)

        event_type = event.get("type")

        if event_type == "session.ready":
            print("✅ AssemblyAI session ready")

        elif event_type == "transcript.user":
            print("👤 You:", event)

        elif event_type == "transcript.agent":
            print("🤖 Agent:", event)

        elif event_type == "reply.audio":
            audio_b64 = event.get("audio")

            if audio_b64:
                audio_bytes = base64.b64decode(audio_b64)

                speaker_buffer.put(audio_bytes)

                print("🔊 Agent audio received")

        elif event_type == "reply.done":
            print("✅ Agent response complete\n")

        elif event_type == "error":
            print("❌ Error:", event)

        else:
            print("SERVER:", event)


async def play_speaker():
    def output_callback(outdata, frames, time, status):
        if status:
            print("Speaker:", status)

        required_bytes = len(outdata)

        try:
            audio_data = speaker_buffer.get_nowait()
        except queue.Empty:
            outdata[:] = b"\x00" * required_bytes
            return

        if len(audio_data) >= required_bytes:
            outdata[:] = audio_data[:required_bytes]

            remaining = audio_data[required_bytes:]

            if remaining:
                speaker_buffer.put_nowait(remaining)

        else:
            outdata[:len(audio_data)] = audio_data

            remaining_bytes = required_bytes - len(audio_data)

            outdata[len(audio_data):] = b"\x00" * remaining_bytes

    with sd.RawOutputStream(
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        channels=CHANNELS,
        dtype="int16",
        callback=output_callback,
    ):
        print("🔊 Speaker started.")

        while True:
            await asyncio.sleep(1)


async def main():
    if not API_KEY:
        raise RuntimeError(
            "ASSEMBLYAI_API_KEY is not set in your .env file"
        )

    print("Connecting to AssemblyAI...")

    async with websockets.connect(
        WS_URL,
        additional_headers={
            "Authorization": f"Bearer {API_KEY}",
        },
    ) as websocket:

        print("Connected.\n")

        await websocket.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "system_prompt": (
                            "You are the Tailgate Quote voice assistant. "
                            "You help field technicians describe jobs "
                            "for accurate quotes. Keep responses short "
                            "and conversational."
                        ),
                        "greeting": (
                            "Hi, I'm Tailgate Quote. "
                            "Tell me about the job you need to quote."
                        ),
                        "output": {
                            "voice": "ivy",
                        },
                    },
                }
            )
        )

        print("session.update sent.\n")

        await asyncio.gather(
            send_microphone(websocket),
            receive_messages(websocket),
            play_speaker(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")