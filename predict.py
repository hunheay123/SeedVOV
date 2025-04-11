from ultralytics import YOLO
import cv2
import pyttsx3
import time

# 음성 엔진 초기화
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# 모델 로드
model = YOLO("runs/train/custom_yolo/weights/best.pt")

# 웹캠 열기
cap = cv2.VideoCapture(0)

last_spoken = {}
speak_interval = 3  # 초

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 객체 감지
    results = model.predict(source=frame, conf=0.05, stream=True)

    for r in results:
        boxes = r.boxes
        names = model.names

        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = names[cls_id]
            print("감지됨:", class_name)
            now = time.time()

            if class_name not in last_spoken or (now - last_spoken[class_name] > speak_interval):
                engine.say(class_name)
                engine.runAndWait()
                last_spoken[class_name] = now

        # 여기서 imshow 실행
        im_array = r.plot()  # 이미지에 박스 그린 결과
        cv2.imshow("YOLOv8 + Voice", im_array)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
