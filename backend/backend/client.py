import cv2
import requests

# YOLO 탐지 결과 가져오기
url = "http://127.0.0.1:5000/detect"
files = {"image": open("test1.jpg", "rb")}
response = requests.post(url, files=files)
detections = response.json()["detections"]

# YOLO 클래스 목록 (COCO 데이터셋 기준, 필요하면 수정!)
CLASS_NAMES = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
               "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", ...]

# 원본 이미지 불러오기
image = cv2.imread("test1.jpg")

# 🔍 탐지된 객체 정보 콘솔 출력 + 이미지에 네모 박스 추가
print("\n🔍 탐지 결과:")
for obj in detections:
    bbox = obj["bbox"]
    class_id = obj["class"]
    confidence = obj["confidence"]

    label = f"{CLASS_NAMES[class_id]}: {confidence:.2f}"

    print(f"객체 클래스: {label}, 위치: {bbox}")  # 콘솔 출력

    cv2.rectangle(image, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
    cv2.putText(image, label, (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 2)

# 이미지 창에서 결과 확인
cv2.imshow("YOLO Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()