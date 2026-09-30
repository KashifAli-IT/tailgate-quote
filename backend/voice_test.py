import asyncio
import base64
import json
import os
import queue

import sounddevice as sd
import websockets
from dotenv import load_dotenv

from backend.app.services.pricing_service import get_price_list

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
    pending_tools = []

    while True:
        raw_message = await websocket.recv()
        event = json.loads(raw_message)

        event_type = event.get("type")

        print(f"\n📡 EVENT: {event_type}")

        if event_type == "session.updated":
            print("✅ Session configuration accepted")
            print("🔧 Tool configuration was accepted by AssemblyAI")
            print("SERVER:", json.dumps(event, indent=2))

        elif event_type == "session.ready":
            print("✅ AssemblyAI session ready")
            print("SERVER:", json.dumps(event, indent=2))

        elif event_type == "transcript.user":
            print("👤 You:", event.get("text", ""))

        elif event_type == "transcript.agent":
            print("🤖 Agent:", event.get("text", ""))

        elif event_type == "tool.call":
            print("🔥 TOOL CALL RECEIVED")

            tool_name = event.get("name")
            call_id = event.get("call_id")
            arguments = event.get("arguments", {})

            print("   Name:", tool_name)
            print("   Call ID:", call_id)
            print("   Arguments:", arguments)

            if tool_name == "get_price_list":
                query = arguments.get("query", "")

                result = {
                    "query": query,
                    "items": get_price_list(query),
                }

                pending_tools.append(
                    {
                        "call_id": call_id,
                        "result": result,
                    }
                )

                print(
                    "   Result prepared:",
                    json.dumps(result, indent=2),
                )

            else:
                print(f"⚠️ Unknown tool requested: {tool_name}")

        elif event_type == "reply.audio":
            audio_b64 = event.get("data")

            if not audio_b64:
                print("⚠️ reply.audio event contains no data")
                continue

            audio_bytes = base64.b64decode(audio_b64)

            speaker_buffer.put(audio_bytes)

        elif event_type == "reply.done":
            status = event.get("status")

            print("✅ Agent response complete")
            print("   Status:", status)

            if status == "interrupted":
                print("⚠️ Reply interrupted — discarding pending tools")
                pending_tools.clear()
                continue

            for tool in pending_tools:
                tool_result_message = {
                    "type": "tool.result",
                    "call_id": tool["call_id"],
                    "result": json.dumps(tool["result"]),
                }

                await websocket.send(
                    json.dumps(tool_result_message)
                )

                print(
                    f"🔧 Tool result sent: {tool['call_id']}"
                )

            pending_tools.clear()

        elif event_type == "session.error":
            print("❌ SESSION ERROR")
            print(json.dumps(event, indent=2))

        elif event_type == "error":
            print("❌ ERROR")
            print(json.dumps(event, indent=2))

        else:
            print("SERVER:", json.dumps(event, indent=2))


async def play_speaker():
    def output_callback(outdata, frames, time, status):
        if status:
            print("Speaker:", status)

        required_bytes = frames * 2  # int16 mono = 2 bytes/sample

        output = bytearray()

        while len(output) < required_bytes:
            try:
                chunk = speaker_buffer.get_nowait()
                output.extend(chunk)
            except queue.Empty:
                break

        if len(output) < required_bytes:
            output.extend(b"\x00" * (required_bytes - len(output)))

        outdata[:] = bytes(output[:required_bytes])

        # If we collected more than needed, preserve the remainder
        extra = output[required_bytes:]

        if extra:
            speaker_buffer.put_nowait(bytes(extra))

    with sd.RawOutputStream(
        samplerate=24_000,
        blocksize=480,
        channels=1,
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
                            "You are Tailgate Quote, a voice-first quoting assistant "
                            "for field service technicians. "

                            "Your job is to help technicians build accurate material quotes. "

                            "CRITICAL PRICING RULE: "
                            "Whenever the technician asks for the price, cost, or catalog "
                            "information for a material or item, you MUST call the "
                            "get_price_list tool before answering. "
                            "If the user asks for a material price, NEVER answer from your own knowledge. ALWAYS call get_price_list first."
                            "NEVER provide a material price from your own knowledge. "
                            "NEVER say that you do not have access to pricing. "
                            "NEVER guess or invent a price. "

                            "Use the exact tool result to answer the technician. "

                            "For example: "
                            "If the technician says 'How much is 3/4 inch copper pipe?', "
                            "immediately call get_price_list with "
                            "{\"query\": \"3/4 inch copper pipe\"}. "

                            "After receiving the tool result, briefly state the matching "
                            "catalog item and its price. "

                            "Keep responses short and conversational."
                        ),
                        "greeting": (
                            "Hi, I'm Tailgate Quote. "
                            "Tell me about the job you need to quote."
                        ),
                        "output": {
                            "voice": "ivy",
                        },
                        "tools": [
                            {
                                "type": "function",
                                "name": "get_price_list",
                                "description": (
                                    "MANDATORY pricing lookup tool. "
                                    "Call this tool whenever the technician asks how much "
                                    "a material or item costs, asks for its price, asks for "
                                    "a rate, or needs catalog pricing for a quote. "
                                    "Never answer a pricing question without calling this tool."
                                ),
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "query": {
                                            "type": "string",
                                            "description": (
                                                "Material or item to search for, "
                                                "such as '3/4 inch copper pipe' "
                                                "or 'shutoff valve'."
                                            ),
                                        }
                                    },
                                    "required": ["query"],
                                },
                            }
                        ],
                    }
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