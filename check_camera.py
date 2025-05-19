import cv2

for i in range(5):  # 여러 카메라 번호 테스트
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"카메라 {i} 사용 가능!")
        cap.release()