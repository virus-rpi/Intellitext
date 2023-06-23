import json
import os
import tempfile
from flask import Flask, send_file, request
import pyttsx3
from pydub import AudioSegment
from deep_translator import GoogleTranslator
from functools import lru_cache

app = Flask(__name__)

audio_cache = {}
target_language = 'en'


@lru_cache
def split_text(text, max_chars):
    print("Splitting")
    sentences = text.split('. ')
    smaller_texts = []
    current_text = ""

    for sentence in sentences:
        if len(current_text) + len(sentence) <= max_chars:
            current_text += sentence + '. '
        else:
            smaller_texts.append(current_text)
            current_text = sentence + '. '

    if current_text:
        smaller_texts.append(current_text)
    print("Splitted")
    return smaller_texts


@lru_cache
def translate_text(text, target_language):
    translation = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translation


@lru_cache
def translate_large_text(text, target_language, max_chars):
    smaller_texts = split_text(text, max_chars)
    translated_chunks = []

    print("Translating")
    for chunk in smaller_texts:
        translated_chunk = translate_text(chunk, target_language)
        translated_chunks.append(translated_chunk)

    translated_text = ' '.join(translated_chunks)
    print("Translated")
    return translated_text


@app.route('/')
def index():
    book_links = ""
    for file in os.listdir():
        if file.endswith(".json"):
            name = os.path.splitext(file)[0]
            book_links += f'<a href="/{name}">{name}</a> <a href="/audio/{name}">(Audio)</a><br>'

    target_languages = ['de', 'en']

    language_options = ""
    for language in target_languages:
        selected = "selected" if language == target_language else ""
        language_options += f'<option value="{language}" {selected}>{language}</option>'

    # Render the index template with the dropdown menu
    return f"""
    <h1>Welcome!</h1>
    <p>Books:</p>
    {book_links}

    <form action="/" method="POST">
        <label for="language">Select Target Language:</label>
        <select name="language" id="language" onchange="this.form.submit()">
            {language_options}
        </select>
    </form>
    """ + """
    <script>
        document.getElementById('language').addEventListener('change', function() {
            this.form.submit();
        });
    </script>
    """


@app.route('/', methods=['POST'])
def set_language():
    global target_language
    target_language = request.form['language']
    return index()


@app.route('/<name>')
def book(name):
    if os.path.isfile(name + ".json"):
        with open(name + ".json", 'r') as f:
            data = json.load(f)

        book_raw = data['book'].split('\n\n')

        book = ""
        for text in book_raw:
            if target_language != 'en':
                text = translate_large_text(data['book'], target_language, 4500)
            book += f"<p>{text}</p>"

        website = f"""
        <h1>{data["name"]}</h1>
        {book}
        """
    else:
        website = "Sorry, that book doesn't exist."
    return website


def combined_audio_files(audio_files, output_path):
    combined_audio = AudioSegment.silent(duration=0)

    for audio_file in audio_files:
        audio_segment = AudioSegment.from_file(audio_file)
        combined_audio += audio_segment

    combined_audio.export(output_path, format="mp3")


def change_voice(engine, language):
    if language == "de":
        language = "DE-DE"
    else:
        language = "EN-US"
    for voice in engine.getProperty('voices'):
        if language in voice.id:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}'not found".format(language))


@app.route('/audio/<name>')
def audio(name):
    if os.path.isfile(name + ".json"):
        with open(name + ".json", 'r') as f:
            data = json.load(f)

        if name in audio_cache:
            # Return the cached audio file if it exists
            return send_file(audio_cache[name], mimetype='audio/mpeg')

        text = ''.join(data['book'])
        if target_language != 'en':
            text = translate_large_text(data['book'], target_language, 4500)

        max_chars = 200
        chapters = split_text(text, max_chars)

        # Generate audio for each chapter
        audio_files = []
        for i, chapter_text in enumerate(chapters):
            chapter_name = f"{name}_chapter_{i + 1}"
            if chapter_name in audio_cache:
                audio_files.append(audio_cache[chapter_name])
            else:
                print("Speaking")
                temp_path = tempfile.mktemp(suffix='.mp3')
                engine = pyttsx3.init()
                change_voice(engine, target_language)
                engine.save_to_file(chapter_text, temp_path)
                engine.runAndWait()
                audio_files.append(temp_path)
                audio_cache[chapter_name] = temp_path

        # Concatenate audio files for all chapters
        combined_audio_path = tempfile.mktemp(suffix='.mp3')
        combined_audio_files(audio_files, combined_audio_path)

        # Serve the combined audio file
        return send_file(combined_audio_path, mimetype='audio/mpeg')

    else:
        return "Sorry, that book doesn't exist."


if __name__ == '__main__':
    app.run(host="192.168.178.53", port=80)
