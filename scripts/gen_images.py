import asyncio
import os
import base64
import sys
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv("/app/backend/.env")

PROMPTS = {
    "kambala_buffalo": (
        "Editorial documentary photograph of two majestic decorated Indian water buffaloes "
        "being gently prepared by their trainer in a lush green paddy field in coastal "
        "Karnataka before Kambala season. Soft warm early-morning golden light, misty air, "
        "mud tracks in the foreground, respectful and calm mood. No people faces in focus, "
        "no race in progress, no aggression. Cinematic 35mm film look, natural earthy palette."
    ),
    "temple_courtyard": (
        "Serene documentary photograph of a peaceful South Indian coastal temple courtyard "
        "at dawn, empty stone floor still wet from morning wash, a single brass oil lamp "
        "flickering, soft pale-golden sunrise light spilling through tall pillars, "
        "jasmine garland on a wooden threshold. Warm, welcoming, gentle mood. "
        "No people, no harsh shadows, no intense fire, no crowd. Muted ochre and cream palette, "
        "shallow depth of field, cinematic 35mm film look."
    ),
}

OUT_DIR = "/app/backend/static/generated"
os.makedirs(OUT_DIR, exist_ok=True)


async def gen(name: str, prompt: str):
    api_key = os.getenv("EMERGENT_LLM_KEY")
    chat = LlmChat(api_key=api_key, session_id=f"custodian-img-{name}", system_message="You generate documentary photographs.")
    chat.with_model("gemini", "gemini-3.1-flash-image-preview").with_params(modalities=["image", "text"])
    msg = UserMessage(text=prompt)
    _text, images = await chat.send_message_multimodal_response(msg)
    if not images:
        print(f"FAIL {name}: no image returned")
        return
    img = images[0]
    image_bytes = base64.b64decode(img["data"])
    path = os.path.join(OUT_DIR, f"{name}.png")
    with open(path, "wb") as f:
        f.write(image_bytes)
    print(f"OK {name} -> {path} ({len(image_bytes)} bytes)")


async def main():
    await asyncio.gather(*[gen(n, p) for n, p in PROMPTS.items()])


if __name__ == "__main__":
    asyncio.run(main())
