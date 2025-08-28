import cv2
print("Start")
cap = cv2.VideoCapture(0)
print("OF")

while True:
    ret, img = cap.read()
    cv2.imshow("wow", img)
    cv2.waitKey(1)
