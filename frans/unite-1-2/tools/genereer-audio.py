"""Genereert de MP3's voor de luistertoets met Voxtral TTS (lokaal, via mlx-audio).

Gebruik (vanuit de repo-root, in een venv met `mlx-audio[tts]`, `mistral-common[audio]`, `soundfile`):
    python frans/unite-1-2/tools/genereer-audio.py          # alleen ontbrekende bestanden
    python frans/unite-1-2/tools/genereer-audio.py --alles  # alles opnieuw
    python frans/unite-1-2/tools/genereer-audio.py --alles --stem m  # alleen de mannenstem opnieuw

Leest de vragen uit index.html (via Node) en schrijft audio/<id>.mp3.
Vereist: node en ffmpeg.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load

GAME_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = GAME_DIR / "audio"
MODEL = "mlx-community/Voxtral-4B-TTS-2603-mlx-bf16"
VOICES = {"f": "fr_female", "m": "fr_male"}
SAMPLE_RATE = 24000
PAUSE_SENTENCE = 0.7  # seconden stilte tussen zinnen
PAUSE_SPEAKER = 1.2   # seconden stilte tussen sprekers in een dialoog
TEMPO = {"f": 0.88, "m": 0.88}  # afspeelsnelheid per stem (toonhoogte blijft gelijk)


def read_questions():
    js = f"""
      const html = require('fs').readFileSync({json.dumps(str(GAME_DIR / 'index.html'))}, 'utf8');
      const src = html.match(/const QUESTIONS = (\\[[\\s\\S]*?\\n\\]);/)[1];
      console.log(JSON.stringify(eval(src)));
    """
    return json.loads(subprocess.check_output(["node", "-e", js]))


def split_sentences(line):
    """Splitst 'Salut. Je suis…' in losse zinnen, zodat er pauzes tussen komen."""
    sentences, current = [], ""
    for char in line:
        current += char
        if char in ".!?" and current.strip():
            sentences.append(current.strip())
            current = ""
    if current.strip():
        sentences.append(current.strip())
    return sentences


def silence(seconds):
    return np.zeros(int(seconds * SAMPLE_RATE), dtype=np.float32)


def speak(model, text, voice):
    parts = [np.array(r.audio, dtype=np.float32) for r in model.generate(text=text, voice=voice)]
    return np.concatenate(parts)


def render_question(model, question):
    """Dialoogregels wisselen van stem, beginnend met question['voice']."""
    order = [question["voice"], "m" if question["voice"] == "f" else "f"]
    chunks = []
    for line_nr, line in enumerate(question["audio"]):
        if line_nr > 0:
            chunks.append(silence(PAUSE_SPEAKER))
        voice = VOICES[order[line_nr % 2]]
        for sentence_nr, sentence in enumerate(split_sentences(line)):
            if sentence_nr > 0:
                chunks.append(silence(PAUSE_SENTENCE))
            chunks.append(speak(model, sentence, voice))
    return np.concatenate(chunks)


def save_mp3(samples, target, tempo):
    with tempfile.NamedTemporaryFile(suffix=".wav") as wav:
        sf.write(wav.name, samples, SAMPLE_RATE)
        subprocess.run(
            ["ffmpeg", "-loglevel", "error", "-y", "-i", wav.name,
             "-af", f"atempo={tempo}", "-codec:a", "libmp3lame", "-q:a", "2", str(target)],
            check=True,
        )


def main():
    regenerate_all = "--alles" in sys.argv
    only_voice = sys.argv[sys.argv.index("--stem") + 1] if "--stem" in sys.argv else None
    AUDIO_DIR.mkdir(exist_ok=True)
    todo = [q for q in read_questions()
            if (only_voice is None or q["voice"] == only_voice)
            and (regenerate_all or not (AUDIO_DIR / f"{q['id']}.mp3").exists())]
    if not todo:
        print("Alle audio is er al.")
        write_audio_list()
        return
    model = load(MODEL)
    for question in todo:
        target = AUDIO_DIR / f"{question['id']}.mp3"
        save_mp3(render_question(model, question), target, TEMPO[question["voice"]])
        print("ok", target.name)
    write_audio_list()


def write_audio_list():
    """audio/lijst.json: de service worker slaat deze MP3's op voor offline gebruik."""
    names = sorted(p.name for p in AUDIO_DIR.glob("*.mp3"))
    (AUDIO_DIR / "lijst.json").write_text(json.dumps(names, indent=0) + "\n")


if __name__ == "__main__":
    main()
