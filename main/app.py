from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
from tensorflow.keras.models import load_model
from PIL import ImageFont, ImageDraw, Image
import mediapipe as mp
import numpy as np
import pandas as pd
import cv2, math

hands = mp.solutions.hands.Hands()
pose = mp.solutions.pose.Pose()
pose_take = [0,11,12,13,14]

name = "M9-3-2025-Uan"

model = load_model(f"ML-model/{name}/model.h5")
with open(f"ML-model/{name}/text.txt", "r", encoding="utf-8") as f:
    class_names = f.read().splitlines()

frame_x = 720
frame_y = 480
frame_get = 10
working=False
Finish=True
collectpic=False
clientcsv=[]
label=""
npic=0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

cap = cv2.VideoCapture(0)

def generate_frames():
    global clientcsv, working, Finish, label, npic
    while True:
        row=[]
        LH=[]
        RH=[]
        RP=[.5,.8]
        
        ret, img = cap.read()
        img = cv2.resize(img, (frame_x, frame_y))
        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
        
        hand_result = hands.process(img)
        pose_results = pose.process(img)
        
        if label !="":
            img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            font = ImageFont.truetype("C:/Users/User/OneDrive/Documents/THSarabunNew/THSarabunNew.ttf", 60)
            draw = ImageDraw.Draw(img_pil)
            draw.text((310, 240), label, font=font, fill=(0, 255, 0))
            img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

        if pose_results.pose_landmarks:
            make=[]
            for id,lm in enumerate(pose_results.pose_landmarks.landmark):
                x, y = lm.x, lm.y
                if id in pose_take:
                    make.extend([x, y])
            RP=[(make[0]+make[2])/2, (make[1]+make[3])/2]
            cv2.circle(img ,(round(RP[0]*frame_x),round(RP[1]*frame_y)), 1, (0,0,255), 7)

        if hand_result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_result.multi_hand_landmarks):
                arx, ary = [], []
                handedness = hand_result.multi_handedness[idx].classification[0].label
                for lm in hand_landmarks.landmark: 
                    x, y= lm.x, lm.y    
                    arx.append(x)
                    ary.append(y)
                    if handedness == "Left" and len(LH)<21:
                        LH.append((math.sqrt((lm.x - RP[0]) ** 2 + (lm.y - RP[1]) ** 2)))
                    if handedness == "Right" and len(RH)<21:
                        RH.append((math.sqrt((lm.x - RP[0]) ** 2 + (lm.y - RP[1]) ** 2)))

                mx = round(max(arx)*frame_x)
                lx = round(min(arx)*frame_x)
                my = round(max(ary)*frame_y)
                ly = round(min(ary)*frame_y)

                cv2.rectangle(img, (lx,ly), (mx,my),(50,150,0), 2)
                cv2.putText(img, str(handedness), (lx, ly), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
                
        if working and Finish and len(clientcsv)<200:
            cv2.putText(img, f"Get: {npic}/200", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
            npic+=1
            if len(LH) <= 0:
                LH = [0 for _ in range(21)]
            row.extend(LH)
            if len(RH) <= 0:
                RH = [0 for _ in range(21)]
            row.extend(RH)
            
            clientcsv.append(row)
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def processs():
    global clientcsv, working, Finish, label, npic
    if not working and Finish and label == "":
        print("start")
        working=True
        clientcsv=[]
    elif working and Finish and label == "" and npic>=30:
        print("stop")
        npic=0
        Finish=False
        socketio.emit("redlighton")
        forpredict=[]
        maxarr=len(clientcsv)
        con = math.floor(maxarr/frame_get)
        for id, ob in enumerate(clientcsv):
            if id%con==0 and len(forpredict)<frame_get*42:
                forpredict.extend(ob)
        pred = model.predict(np.array([forpredict]).reshape(1, -1))
        index = np.argmax(pred)
        label = class_names[index]
        working=False
        Finish=True
        socketio.emit("next")

@app.route('/')
def index():
    return render_template('displayindex.html')

@app.route('/laptop') 
def laptop(): 
    return render_template("webindex.html")

@app.route('/video')  
def video(): 
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('laptopmessage')
def handle_message(msg):
    print(msg) 
    emit("take", (msg, "laptop"), broadcast=True) 

@socketio.on('dismessage')
def handle_message(currenttext):
    global label
    if label == "" and currenttext != "":
        emit("take", (currenttext, "ipad"), broadcast=True) 
    elif label != "":
        emit("add_text", label, broadcast=True)
        label = ""

@socketio.on('work')
def newwork():
    pass
        
@socketio.on('fordelete')
def deletelabel():
    global label
    label=""
    
@app.route('/send', methods=['POST'])
def addonsend():
    socketio.emit("addonbtn")
    return "ok"
@app.route('/cancel', methods=['POST'])
def addoncancel():
    deletelabel()
    return "ok"
@app.route('/start', methods=['POST'])
def startwork():
    print("on")
    processs()
    return "ok"


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)