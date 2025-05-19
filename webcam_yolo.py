import cv2
import torch
from yolov5 import YOLOv5

# YOLO 모델 로드
model = YOLOv5("yolov5s.pt", device="cpu")  # GPU 사용 가능하면 "cuda"로 변경

# 웹캠 열기q
cap = cv2.VideoCapture(1)  # 기본 웹캠 (외장 카메라 사용 시 번호 변경)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 객체 탐지 실행 (수정된 부분!)
    results = model.predict(frame)  # ✅ `.predict()` 사용!

    # 탐지된 객체를 화면에 표시
    for *box, conf, cls in results.xyxy[0].tolist():
        cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
        label = f"{model.model.names[int(cls)]}: {conf:.2f}"  # ✅ 수정된 부분!
        cv2.putText(frame, label, (int(box[0]), int(box[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.5, (0, 255, 0), 2)

    cv2.imshow("YOLO Real-time Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):  # 'q' 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()