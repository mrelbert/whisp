from flask import Flask, render_template
import sounddevice as sd
import soundfile as sf
import openai

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/record', methods=['POST'])
def record():
    duration = 5  # seconds
    filename = 'output.wav'
    samplerate = 44100
    channels = 1
    myrecording = sd.rec(int(duration * samplerate),
                         samplerate=samplerate, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, samplerate)

    audio_file = open("output.wav", "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    print(transcript)

    return render_template('result.html', text=transcript['text'])


if __name__ == '__main__':
    app.run()
