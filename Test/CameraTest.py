import cv2
from ultralytics import YOLO

# YOLO 모델 로드 (yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt 등 선택 가능)
model = YOLO('yolov8n.pt')  # 가장 가벼운 모델

# 웹캠 열기 (기본 내장 카메라는 device index 0)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 모델에 프레임 전달
    results = model(frame)

    # 결과 이미지에 Bounding Box 그리기
    annotated_frame = results[0].plot()

    # 화면에 표시
    cv2.imshow('YOLOv8 - Webcam', annotated_frame)

    # ESC 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
