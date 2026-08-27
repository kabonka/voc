import asyncio, json, os
import edge_tts

VOICE = "en-US-JennyNeural"  # 清晰的英文女声，适合学习
BASE = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(BASE, "audio")
os.makedirs(AUDIO, exist_ok=True)

with open(os.path.join(BASE, "words.json"), "r", encoding="utf-8") as f:
    words = json.load(f)

async def gen(text, path):
    if not text or not text.strip():
        return
    comm = edge_tts.Communicate(text, VOICE)
    await comm.save(path)

async def main():
    sem = asyncio.Semaphore(2)
    done = 0
    async def worker(idx, kind, text):
        nonlocal done
        path = os.path.join(AUDIO, f"w{idx:03d}_{kind}.mp3")
        if os.path.exists(path) and os.path.getsize(path) > 0:
            done += 1
            return
        async with sem:
            for attempt in range(20):
                try:
                    await gen(text, path)
                    if os.path.exists(path) and os.path.getsize(path) > 0:
                        done += 1
                        break
                except Exception as e:
                    if attempt < 19:
                        await asyncio.sleep(2.0 * (attempt + 1))
                    else:
                        print(f"ERR {idx} {kind}: {e}")
    tasks = []
    for idx, w in enumerate(words):
        for kind in ("word", "def", "sent"):
            tasks.append(worker(idx, kind, w.get(kind, "")))
    await asyncio.gather(*tasks)
    print(f"DONE ({done} files)")

asyncio.run(main())
