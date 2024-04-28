import whisper
model = whisper.load_model("base")
result = model.transcribe("rec.flac")
print(f' The text in video: \n {result["text"]}')