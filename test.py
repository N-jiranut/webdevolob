import mediapipe as mp
import cv2, os, time, math

hands = mp.solutions.hands.Hands()
pose = mp.solutions.pose.Pose()
pose_take = [0]
frame_x, frame_y = 720, 480

def mian(camera):
    cap = cv2.VideoCapture(camera)
    # frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    while True:
        ret, img = cap.read()
        if not ret:
            print("video end")
            break
        img = cv2.resize(img, (frame_x, frame_y))
        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hand_result = hands.process(img)
        pose_result = pose.process(img)
        main_point = None
        row=[]
        
        if pose_result.pose_landmarks:
            for id, lm in enumerate(pose_result.pose_landmarks.landmark):
                if id == 0:
                    main_point = [lm.x, lm.y]
                if id in pose_take:
                    cx, cy = int(lm.x * frame_x), int(lm.y * frame_y)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        if hand_result.multi_hand_landmarks:
            for idx, hand_landmark in enumerate(hand_result.multi_hand_landmarks):
                mp.solutions.drawing_utils.draw_landmarks(frame,hand_landmark,mp.solutions.hands.HAND_CONNECTIONS)
                handedness = hand_result.multi_handedness[idx].classification[0].label
                for id, lm in enumerate(hand_landmark.landmark):
                    if handedness == "Right":
                        row.append(math.sqrt((lm.x - main_point[0]) ** 2 + (lm.y - main_point[1]) ** 2))
                        
        cv2.imshow("img", img)
        cv2.waitKey(1)

path="video"
class_file = os.listdir("video")
for classs in class_file:
    video_path = os.path.join(path, classs)
    videos = os.listdir(video_path)
    for video in videos:
        video_file = os.path.join(video_path, video)
        
        mian(video_file)