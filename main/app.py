from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
from tensorflow.keras.models import load_model
import mediapipe as mp
import numpy as np
import pandas as pd
import cv2, math

hands = mp.solutions.hands.Hands()
pose = mp.solutions.pose.Pose()

name = "M9-3-2025-tree100"

from pytorch_tabnet.tab_model import TabNetClassifier

# Create a new instance
tabnet_loaded = TabNetClassifier()
tabnet_loaded.load_model(f"{name}/tabnet_model.zip")

# Now you can use tabnet_loaded to predict:
# y_pred = tabnet_loaded.predict(X_test)

# model = load_model(f"{name}/model.h5")
with open(f"{name}/text.txt", "r") as f:
    class_names = f.read().splitlines()
pose_take = [0,11,12,13,14,15,16]

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

# def startwork():
#     global clientcsv, working, Finish, class_names, label, npic
#     print("on")
#     if not working and Finish and label == "":
#         working=True
#         clientcsv=[]
#     elif working and Finish and label == "" and npic>=30:
#         npic=0
#         Finish=False
#         emit("redlighton", broadcast=True)
#         forpredict=[]
#         maxarr=len(clientcsv)
#         con = math.floor(maxarr/15)
#         for id, ob in enumerate(clientcsv):
#             if id%con and len(forpredict)<1470:
#                 forpredict.extend(ob)
#         pred = model.predict(np.array([forpredict]).reshape(1, -1))
#         index = np.argmax(pred)
#         label = class_names[index]
#         working=False
#         Finish=True
#         emit("next", broadcast=True)

def generate_frames():
    global clientcsv, working, Finish, label, npic
    while True:
        row=[]
        LH=[]
        RH=[]
        BO=[]
        ret, frame = cap.read()
        frame = cv2.resize(frame, (720, 480))
        frame = cv2.flip(frame, 1)
        img = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        if label !="":
            cv2.putText(frame, label, (310, 240), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
        hand_result = hands.process(img)
        pose_results = pose.process(img)
        if hand_result.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(hand_result.multi_hand_landmarks):
                arx, ary = [], []
                handedness = hand_result.multi_handedness[idx].classification[0].label
                for lm in hand_landmarks.landmark: 
                    x, y= lm.x, lm.y    
                    arx.append(x)
                    ary.append(y)
                    if handedness == "Left" and len(LH)<42:
                        LH.extend([x,y])
                    if handedness == "Right" and len(RH)<42:
                        RH.extend([x,y])

                mx = round(max(arx)*720)
                lx = round(min(arx)*720)
                my = round(max(ary)*480)
                ly = round(min(ary)*480)

                cv2.rectangle(frame, (lx,ly), (mx,my),(50,150,0), 2)
                cv2.putText(frame, str(handedness), (lx, ly), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2, cv2.LINE_AA)
         
        if pose_results.pose_landmarks:
            landmarks = pose_results.pose_landmarks.landmark
            for id,lm in enumerate(landmarks):
                x, y = lm.x, lm.y
                if id in pose_take:
                    cv2.circle(frame ,(round(x*720),round(y*480)), 1, (0,0,255), 7)
                    BO.extend([x, y])    
                
        if working and Finish and len(clientcsv)<200:
            cv2.putText(frame, f"Get: {npic}/200", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2, cv2.LINE_AA)
            npic+=1
            if len(LH) <= 0:
                LH = [0 for _ in range(42)]
            row.extend(LH)
            if len(RH) <= 0:
                RH = [0 for _ in range(42)]
            row.extend(RH)  
            if len(BO) <= 0:
                BO = [0 for _ in range(14)]      
            row.extend(BO)
            clientcsv.append(row)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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
    global clientcsv, working, Finish, class_names, label, npic
    print("on")
    if not working and Finish and label == "":
        working=True
        clientcsv=[]
    elif working and Finish and label == "" and npic>=30:
        npic=0
        Finish=False
        socketio.emit("redlighton")
        forpredict=[]
        maxarr=len(clientcsv)
        con = math.floor(maxarr/15)
        for id, ob in enumerate(clientcsv):
            if id%con and len(forpredict)<1470:
                forpredict.extend(ob)
        pred = model.predict(np.array([forpredict]).reshape(1, -1))
        index = np.argmax(pred)
        label = class_names[index]
        working=False
        Finish=True
        socketio.emit("next")
    return "ok"


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)