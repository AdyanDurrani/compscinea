import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Camera not being read")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("can not read camera.")
        break

    cv.imshow("frame", frame)

    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
