# 사전 준비 터미널에 작성하기
# pip install ultralytics opencv-python pyttsx3
# pip install opencv-python
# get-pip.py 내용
import urllib.request
exec(urllib.request.urlopen('https://bootstrap.pypa.io/get-pip.py').read())

#####################################
import cv2
from ultralytics import YOLO
import pyttsx3
import time

# YOLOv8 모델 불러오기
model = YOLO("yolov8n.pt")  # yolov8n.pt는 가장 가벼운 모델

# TTS 초기화
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # 말하는 속도
engine.setProperty('voice', engine.getProperty('voices')[0].id)  # 기본 목소리 사용

# 웹캠 연결
cap = cv2.VideoCapture(0)

# 최근 말한 객체 저장 (중복 방지용)
last_spoken = {}
cooldown = 3  # 3초 동안 같은 객체 말하지 않음

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv8 추론
    results = model(frame)

    # 인식된 객체 처리
    for result in results:
        boxes = result.boxes
        names = model.names

        for box in boxes:
            cls_id = int(box.cls[0])
            label = names[cls_id]
            confidence = float(box.conf[0])

            if confidence < 0.5:
                continue  # 너무 확신 낮으면 무시

            now = time.time()
            # 같은 객체 중복 발화 방지
            if label not in last_spoken or now - last_spoken[label] > cooldown:
                print(f"인식됨: {label}")
                engine.say(f"{label} 입니다")
                engine.runAndWait()
                last_spoken[label] = now

    # 화면에 프레임 띄우기
    cv2.imshow("YOLO 실시간 감지", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
