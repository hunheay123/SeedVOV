# TTS기능 : pip install pyttsx3

import cv2
from ultralytics import YOLO
import pyttsx3
import time

# TTS 초기화
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # 말하는 속도 조절

# YOLO 모델 로드
model = YOLO('yolov8n.pt')  # 또는 'best.pt'로 변경

# 웹캠 열기
cap = cv2.VideoCapture(0)

# 중복 음성 방지를 위한 최근에 말한 객체 기억용
last_spoken = {}
speak_interval = 3  # 같은 객체는 최소 3초 지나야 다시 말함

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 감지
    results = model(frame)[0]

    # Bounding box 그리기
    annotated_frame = results.plot()

    # 인식된 객체 이름 추출 및 음성 출력
    current_time = time.time()
    for box in results.boxes:
        cls_id = int(box.cls[0])  # 클래스 ID
        cls_name = model.names[cls_id]  # 클래스 이름

        # 말한지 3초 지난 경우에만 다시 말함
        if cls_name not in last_spoken or (current_time - last_spoken[cls_name]) > speak_interval:
            print(f"Detected: {cls_name}")
            engine.say(cls_name)
            engine.runAndWait()
            last_spoken[cls_name] = current_time

    # 영상 출력
    cv2.imshow('YOLOv8 - Webcam with Voice', annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
