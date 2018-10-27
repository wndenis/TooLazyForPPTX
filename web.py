from bottle import route, run, template, post, response, request
import speech_recognition as sr

# worker(guid)
# workers
# get worker by cookie(guid) -> delegate
# else - create worker with new guid, send cookie(guid) and -> delegate
temp = """
<!DOCTYPE HTML>
<html>
 <head>
  <meta charset="utf-8">
  <title>TooLazyForPPTX</title>
 </head>
 <body>

  <h1>
  <Center>
  <b>Hello there!</b>
  <br>
  This is mock page for \"TooLazyForPPTX\"!
  <script src=\"https://rawgit.com/mattdiamond/Recorderjs/master/dist/recorder.js\"></script>
  </Center>
  </h1>
 </body>
</html>"""

@route('/')
@route('/test')
def index():
    return template(temp)

from bottle import error
@error(404)
def error404(error):
    return 'Nothing here, sorry'


@post('/api/upload')
def upload():
    #if request.headers['Content-Type'] =
    print(request.json)
    # try:
    #     print(request.json())
    # except:
    #     response.status = 400
    #     return
    response.headers['Content-Type'] = "application/json"
    return {"kek": "data"}


def webRec():
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    result_text = ""

    #obtain audio from the microphone
    r = sr.Recognizer()
    r.energy_threshold = 175
    with sr.Microphone() as source:
        print("Calibrating...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Say something!")
        audio = r.listen(source)
    print("Listening finished")

    try:
        result_text = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said \"" + result_text + "\"")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))





run(host='localhost', port=8080)