import whisper
import yt_dlp
import os

# URL específica del video 
URL_VIDEO = "https://www.youtube.com/watch?v=pXck4dbK-I8"
AUDIO_DIR = "audios"
OUTPUT_DIR = "transcripciones"

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f'{AUDIO_DIR}/audio_input.%(ext)s', 
    'ffmpeg_location': r'C:\ProgramData\chocolatey\bin',
}

try:
    print("--- PASO 1: Descargando audio ---")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([URL_VIDEO])

    audio_path = os.path.join(AUDIO_DIR, "audio_input.mp3")

    print(f"\n--- PASO 2: Transcribiendo con Whisper ---")
    modelo = whisper.load_model("small")
    resultado = modelo.transcribe(audio_path, language="es", fp16=False)

    nombre_base = "fantini-peter-thiel-argentina"
    with open(f"{OUTPUT_DIR}/{nombre_base}.txt", "w", encoding="utf-8") as f:
        f.write(resultado["text"].strip())

    print(f"\n✅ ÉXITO: Archivo generado en {OUTPUT_DIR}/{nombre_base}.txt")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
