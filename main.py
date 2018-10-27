#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

pronouncedText = ""

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

if False:
    #obtain audio from the microphone
    r = sr.Recognizer()
    r.energy_threshold = 175
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    print("Listening finished")



# recognize speech using Google Speech Recognition
if False:
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        pronouncedText = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said \"" + pronouncedText + "\"")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

pronouncedText = "The other day I went to the park and I meet my old friend, her name was Mary. I haven't seen her for years and I was very happy with this encounter. We decided to go for a walk together and later that day we wanted to see a movie at 5pm. However, an hour later, we meet another old friend of hers and it was also quite sudden. So, we changed our plans once again and decided to go to the restaurant that was across the street."

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