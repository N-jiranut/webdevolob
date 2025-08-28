from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send, emit
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

cap = cv2.VideoCapture(0)
def generate_frames():
    while True:
        ret, frame = cap.read()
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

@socketio.on('mainmessage')
def handle_message(msg, user):
    print(msg)
    print(user)
    emit("take", (msg, user), broadcast=True) 

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)