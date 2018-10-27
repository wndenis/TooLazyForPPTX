import speech_recognition as sr
from flask import Flask, render_template, request, make_response
import uuid
import asyncio
import websockets

app = Flask(__name__)


async def connection(websocket, path):
    async for message in websocket:
        await websocket.send(message)

@app.route('/')
def index():
    return render_template("main.html")


@app.route('/auth/', methods=['GET'])
def auth():
    session_id = request.cookies.get("session_id")
    print(session_id)
    if session_id is None:
        print("unknown user")
        resp = make_response()
        session_id = str(uuid.uuid4())
        resp.set_cookie('session_id', session_id)
    else:
        print("known user")

    address = 'localhost/' + session_id
    print(address)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(connection, address, 8765))
    asyncio.get_event_loop().run_forever()
    # SOCKET
    return address + ":8765"







if __name__ == '__main__':
    app.run(debug=True, port=8080)
exit()
# worker(guid)
# workers
# get worker by cookie(guid) -> delegate
# else - create worker with new guid, send cookie(guid) and -> delegate
#
# @error(404)
# def error404(error):
#     return 'Nothing here, sorry'
#
#
# @post('/api/upload')
# def upload():
#     #if request.headers['Content-Type'] =
#     print(request.json)
#     # try:
#     #     print(request.json())
#     # except:
#     #     response.status = 400
#     #     return
#     response.headers['Content-Type'] = "application/json"
#     return {"kek": "data"}

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


"""
register 
login
sendaudiofragment
updatesllides
https://realtimeboard.com/app/board/o9J_kyr359w=/
"""