from flask import Flask, render_template
from flask.json import jsonify
import os
import uuid
import nltk
import heapq
from google_images_download import google_images_download
TEXT = ""
OLD_TEXT = ""
SIMPLIFIED_TEXT = ""
TITLE = ""
IMAGE_ENTITY = ""
IMAGE_LINK = ""

img_google_response = google_images_download.googleimagesdownload()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("main.html")


@app.route('/update', methods=["GET", "POST"])
def getSlides():
    global SIMPLIFIED_TEXT, TEXT, OLD_TEXT
    print("SENDING: " + TEXT)
    if not True and (OLD_TEXT == TEXT):
        OLD_TEXT = TEXT
        std_text = re.sub(r'\[[0-9]*\]', ' ', TEXT)
        std_text = re.sub(r'\s+', ' ', std_text)

        formatted_text = re.sub('[^a-zA-Z]', ' ', std_text)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)

        sentences = nltk.sent_tokenize(formatted_text)

        stopwords = nltk.corpus.stopwords.words('english')
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequency = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequency)

        sentence_scores = {}
        for sent in sentences:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(2, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        SIMPLIFIED_TEXT = summary

    return jsonify({"text": TEXT, "title": TITLE, "image_link": IMAGE_LINK, "simplified_text": SIMPLIFIED_TEXT})

# @app.route('/auth/', methods=['GET'])
# def auth():
#     session_id = request.cookies.get("session_id")
#     print(session_id)
#     if session_id is None:
#         print("unknown user")
#         resp = make_response()
#         session_id = str(uuid.uuid4())
#         resp.set_cookie('session_id', session_id)
#     else:
#         print("known user")
#
#     address = 'ws://localhost/' + session_id
#     print(address)
#     # loop = asyncio.new_event_loop()
#     # asyncio.set_event_loop(loop)
#     # asyncio.get_event_loop().run_until_complete(
#     #     websockets.serve(connection, address, 8765))
#     # asyncio.get_event_loop().run_forever()
#     # SOCKET
#     return address + ":8765"

#============================================================================


import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    global TEXT, IMAGE_ENTITY, TITLE, IMAGE_LINK, SIMPLIFIED_TEXT
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            pass
            # sys.stdout.write(transcript + "\n")  # + overwrite_chars + '\r')
            # sys.stdout.flush()

            # num_chars_printed = len(transcript)

        else:
            #print(transcript + overwrite_chars)

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            num_chars_printed = 0
        if re.search(r'\b(следующий слайд|далее|next|go further|go forward)\b', transcript, re.I):
            transcript = "  "
            TITLE = "  "
            IMAGE_LINK = "  "
            IMAGE_ENTITY = "  "
            SIMPLIFIED_TEXT = "  "

        titleres = re.search("(заголовок|title is|theme is) ([\wа-яА-Я]+)", transcript, re.I)
        if titleres:
            TITLE = titleres.group(2)
            transcript = transcript[:titleres.start(2)] + transcript[titleres.end(2):]
            if len(transcript) == 0:
                transcript = " "

        img2res = re.search("((image|picture) of (how|)) ([\wа-яА-Я]+) looks like", transcript, re.I)
        #boy blowing on candles
        if img2res:
            print("*" * 60)
            if len(img2res.group(3)) > 2:
                IMAGE_ENTITY = img2res.group(3)
                transcript = transcript[:img2res.start(3)] + transcript[img2res.end(3):]
                if len(transcript) == 0:
                    transcript = " "
                IMAGE_LINK = img_google_response.download({"limit": 1, "keywords": IMAGE_ENTITY,
                                                           "time": "past-7-days", "print_urls": True})
                print("#######:\t" + transcript)

        imgres = re.search("(изображени[ея]|выглядит|picture of|image of) ([\wа-яА-Я]+)", transcript, re.I)
        if imgres:
            print("*" * 60)
            if len(imgres.group(2)) > 2:
                IMAGE_ENTITY = imgres.group(2)
                transcript = transcript[:imgres.start(2)] + transcript[imgres.end(2):]
                if len(transcript) == 0:
                    transcript = " "
                IMAGE_LINK = img_google_response.download({"limit": 1, "keywords": IMAGE_ENTITY,
                                                                     "time": "past-7-days", "print_urls": True})
                print("#######:\t" + transcript)



        #print("%s %s" % (transcript, len(transcript)))
        if len(transcript) == 0:
            transcript = TEXT
        TEXT = transcript


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    language_code = 'en-US'  # a BCP-47 language tag
    # language_code = 'ru-RU'  # a BCP-47 language tag
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\\Users\\RealityShift24\\TooLazyForPPTX-3785c34de4cc.json"
    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (types.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)

import threading
import time
def voiceControl():
    while True:
        try:
            print("Voice started")
            main()
        except Exception as e:
            print("restart voice: %s" % e)



voice_thread = threading.Thread(target=voiceControl)
voice_thread.start()
app.run(debug=True, port=8080)

#voice_thread.start()


