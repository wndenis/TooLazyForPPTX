#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

pronouncedText = ""

if False:
    #obtain audio from the microphone
    r = sr.Recognizer()
    r.energy_threshold = 150
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
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
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = r"""{
  "type": "service_account",
  "project_id": "toolazyforpptx",
  "private_key_id": "3785c34de4cc23dd88f467220656e4e5bf153406",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCoDz8Pg8ICO2YQ\nTN8o1QXEujOkyM20jpdzRupQI+4OFqohRe0vOzq7I1lpRIfKuEAp9J+SDuIPbY1z\nQuuAzsZh6qxLFvJT8R8tcqhdhUYjjhdImAOYJ/VV/XHnt0IguKd/iMPWQX2VY8/y\nlqx4diNZXGbokquKJpLGh5JIW9fyaVjig+Ih6zCM4SUBY3fuE8H+X1sf+Mjrzj+y\nNHamifgg4aJYIC72xf8qOCxbm8EhLkykzXzmjt53RsiFf1ntCuozM3G+K8HWWcCg\n6LIpFJIyFGa5Az4IQeMww6Q9FkIPDm6gKA4k0NDMxGtf/o1aulZYitOzn5Sgv2L0\niFV2x6ojAgMBAAECggEASAeo1oR5Ta2ZtBjOeNi8jTHlWpY6HE4VOXJGkSylJmKu\nbm5jFyBCrtyawNR/gvJvhcvz7Iz2dPhWbPVcrKtzOZp0WAawvCuXWkpPQS4S/sAy\n2IlW2QsfSsjC3jacYBvkpnO+xADzy2ipQuczarnvsqg47yuV3DNmKzMGDn9W0e2F\nHRmrF2SJbrKmL+FzWDSa4SNOdEDl82CcAPuRlt+q4bvuXweny2JU31TaSN3oXbRy\ngqACiHZHaV/An0lAjw964UJmxas85X8g3ruJGOf6rb6HlKENxtK+hB23I5ieULvk\nzhJ4MmYzkk3oLbef847BrLSVdCyvDWuLxFJ2hy6GgQKBgQDXi9iuuZIPNeB/HNoj\nMX9TSsHgZEWA1h87oxfb0WPRAxUz8VBzNrzApDavi7rjRteFrSy0q4DmxiA6s5Tz\n/T9APvWjRz8Zhr4IJH/5RzBIjuP9gZP4ZtUeev9wrFBiCgcDk9f9y3HUhe1ipyAY\nE/RC3BbmtLpCVtUUrQ15BvyBQQKBgQDHmdlluY5pX7b0RG+jC9pVzgjc688vutl7\nrGTdFifzUYowyHBuWsntfrVFh5zUThieWJYCEn2IJCOXjaKxCEQYaFvhzbdFs3y2\nPHGxGq3///ByX+KrGLrjudHqXnnBtnchm9Oe0Y+1ZLYAPZP91lj0E1JgR4qU3V9c\n49XwAeguYwKBgCUTeBUt9HLLWK9kvhz5oaYpIMpBVTdBHaQ7fJoiHWJRfm8t3iHD\nU5prZMCzb1Uy1VW4IQ1+xrBrehW+2CtT73JUohoQ4ki4xa1O4fh2B1cjxRHRHSvI\nPHZ+v7uY2EbU5Ln3z1pniU/+LYQfrUSXAhgSFZpfkf5hQ0vILJ4Z1otBAoGASJ90\nluuFoldd9NA1oig8331ggikWMDKW0MWvyTU3gfNICWnUZoKH9+5jPBIUgLaNhIeM\nxOI/ZFppzMmOyUTNqefGjojPxv+AP7oMT7j6WCuiK6sxiLktvo+sjc6kFFQ0Ujkl\nLSLoW8Jx6fJ9txzXLq8dCMTe6j0FZoHLJFE9TisCgYAto6NK1uRQW2ECucar2zVc\nZ7rRsVCrCnnFRQMRnMQNEZPsECUujopZb60W1nB9SykPlDP0oPHLwexrLf9OGqqL\nvDBhvRpiIfTHLMlXEuRRs9POZjmBYBShh6Esmx9WtS5tpIhLMRfIKd3zutJaTMWt\nykMYroNBYn/HjH3P9YiY+Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "toolazyforpptx@toolazyforpptx.iam.gserviceaccount.com",
  "client_id": "117951032280821637676",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/toolazyforpptx%40toolazyforpptx.iam.gserviceaccount.com"
}
"""
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        pronouncedText = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
        print("Google Speech Recognition thinks you said \"" + pronouncedText + "\"")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

print()
print(pronouncedText)
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