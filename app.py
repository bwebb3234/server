from flask import Flask, request, send_file
from flask_cors import CORS
from pytube import YouTube
from moviepy.editor import VideoFileClip
import os
import tempfile

app = Flask(__name__)

# Replace with your actual domain to restrict CORS (or use "*" carefully)
CORS(app, origins=["https://www.your-website.com"])

@app.route('/convert', methods=['POST'])
def convert():
    url = request.form.get('url')
    if not url:
        return {"error": "No URL provided"}, 400

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            return {"error": "No audio stream found"}, 400

        # Use temporary directory to avoid naming conflicts and for cleanup
        with tempfile.TemporaryDirectory() as tmpdirname:
            video_path = audio_stream.download(output_path=tmpdirname, filename='temp_audio')
            mp3_path = os.path.join(tmpdirname, 'converted_audio.mp3')

            video_clip = VideoFileClip(video_path)
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(mp3_path)
            audio_clip.close()
            video_clip.close()

            # Send MP3 file with proper name and mimetype
            return send_file(
                mp3_path,
                as_attachment=True,
                download_name=f"{yt.title}.mp3",
                mimetype="audio/mpeg"
            )

    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)