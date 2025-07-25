from flask import Flask, request, send_file
from flask_cors import CORS
from pytube import YouTube
from pydub import AudioSegment
import os
import tempfile

app = Flask(__name__)
CORS(app, origins=["https://www.webylabz.space"])

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not audio_stream:
            return {"error": "No audio stream found"}, 400

        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = audio_stream.download(output_path=tmpdir, filename='audio')
            
            # pydub will autodetect format based on file extension; 
            # but sometimes pytube downloads .webm or .m4a — pydub supports both if ffmpeg is installed.
            audio = AudioSegment.from_file(input_path)
            
            output_path = os.path.join(tmpdir, "converted_audio.mp3")
            audio.export(output_path, format="mp3")

            return send_file(
                output_path,
                as_attachment=True,
                download_name=f"{yt.title}.mp3",
                mimetype="audio/mpeg"
            )
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
