import json
import os
import tempfile
from flask import Flask, send_file
from gtts import gTTS

app = Flask(__name__)

# Create a dictionary to store cached audio files
audio_cache = {}


@app.route('/')
def index():
    book_links = ""
    for file in os.listdir():
        if file.endswith(".json"):
            name = os.path.splitext(file)[0]
            book_links += f'<a href="/{name}">{name}</a> <a href="/audio/{name}">(Audio)</a><br>'

    return f"""
    <h1>Welcome!</h1>
    <p>Books:</p>
    {book_links}
    """


@app.route('/<name>')
def book(name):
    if os.path.isfile(name + ".json"):
        with open(name + ".json", 'r') as f:
            data = json.load(f)
        website = f"""
        <h1>{data["name"]}</h1>
        <p>{data["book"]}</p>
        """
    else:
        website = "Sorry, that book doesn't exist."
    return website


@app.route('/audio/<name>')
def audio(name):
    if os.path.isfile(name + ".json"):
        with open(name + ".json", 'r') as f:
            data = json.load(f)

        if name in audio_cache:
            # Return the cached audio file if it exists
            return send_file(audio_cache[name], mimetype='audio/mpeg')

        tts = gTTS(data["book"])

        temp_fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(temp_fd)

        tts.save(temp_path)
        audio_cache[name] = temp_path  # Cache the generated audio file

        return send_file(temp_path, mimetype='audio/mpeg')
    else:
        return "Sorry, that book doesn't exist."


if __name__ == '__main__':
    app.run()
