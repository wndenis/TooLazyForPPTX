#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
pronouncedTexts = []

if False:
    #obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Say something!")
        audio = r.listen(source, )
    print("Listening finished")

if True:
    from os import path
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "voice.wav")
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)


#listen_in_background


# recognize speech using Google Speech Recognition
if True:

    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        pronouncedTexts.append(r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS))
        print("Google Speech Recognition thinks you said \"" + pronouncedTexts[-1] + "\"")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

print()
print(pronouncedTexts)
exit()
#NLTK
if False:
    import nltk
    tokens = nltk.word_tokenize(pronouncedText)
    tagged = nltk.pos_tag(tokens)
    print(tagged)
    entities = nltk.chunk.ne_chunk(tagged)
    print(entities)

    from nltk.corpus import treebank
    entities.draw()

    exit()
#NLTK END


#spacy
import spacy
# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load('en_core_web_sm')
doc = nlp(pronouncedText)
# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)

exit()

from spacy import displacy

displacy.serve(doc, style='dep')

print("end")
exit()
# Determine semantic similarities
doc1 = nlp(u"my fries were super gross")
doc2 = nlp(u"such disgusting fries")
similarity = doc1.similarity(doc2)
print(doc1.text, doc2.text, similarity)
exit()
#spacy end