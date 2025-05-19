import cv2

cap = cv2.VideoCapture(1)  # 외장 카메라 사용

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("카메라에서 프레임을 읽을 수 없음! 포트 번호 확인 필요!")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  
        break

cap.release()
cv2.destroyAllWindows()