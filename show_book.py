import json
import os
import tempfile
from flask import Flask, send_file
from gtts import gTTS

app = Flask(__name__)


@app.route('/<name>')
def index(name):
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

        tts = gTTS(data["book"])

        temp_fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(temp_fd)

        tts.save(temp_path)
        return send_file(temp_path, mimetype='audio/mpeg')
    else:
        return "Sorry, that book doesn't exist."


if __name__ == '__main__':
    app.run()
