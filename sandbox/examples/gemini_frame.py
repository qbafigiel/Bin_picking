import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Nie można otworzyć kamery")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Brak klatki z kamery")
        break

    cv2.imshow("Gemini RGB", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
