# from flask import Flask, request, jsonify, render_template
# import torch
# import cv2
# import numpy as np
# from PIL import Image

# # YOLOv5 모델 로드
# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# # Flask 서버 초기화
# app = Flask(__name__)

# # 🔹 웹 UI 렌더링 (웹캠 활성화 포함)
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route('/detect', methods=['POST'])
# def detect():
#     if 'image' not in request.files:
#         return jsonify({'error': 'No image uploaded'}), 400
    
#     # 이미지 받기
#     image_file = request.files['image']
#     image = Image.open(image_file)

#     # YOLOv5로 객체 탐지 수행
#     results = model(image)

#     # 탐지된 객체 정보 추출
#     objects = []
#     for *box, conf, cls in results.xyxy[0].tolist():
#         objects.append({
#             "bbox": box,
#             "confidence": conf,
#             "class": int(cls)
#         })

#     return jsonify({'detections': objects})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

# app.py (yoloproject/backend/app.py)

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import torch
import json
import base64
import cv2
import numpy as np

# Flask 앱 초기화
app = Flask(__name__)
# SocketIO 초기화 (CORS 허용)
socketio = SocketIO(app, cors_allowed_origins="*")

# YOLOv5 모델 로드 (ultralytics hub 사용)
model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=False)
model.eval()

# 루트 경로: index.html 렌더링 (프론트 화면)
@app.route("/")
def index():
    return render_template("index.html")

# 웹소켓 이벤트 "image" 받았을 때 실행되는 함수
@socketio.on("image")
def handle_image(message):
    print("🔍 받은 데이터:", message)  # 디버깅용, 클라이언트에서 온 이미지 데이터(문자열)

    try:
        # JSON 문자열을 파이썬 dict로 변환
        data = json.loads(message)

        # data["image"]는 "data:image/jpeg;base64,..." 형태임
        # ',' 기준으로 나눠서 실제 base64 인코딩된 부분만 분리
        base64_data = data["image"].split(",")[1]

        # base64 문자열 디코딩 → 바이트 배열로 변환
        image_bytes = base64.b64decode(base64_data)

        # 바이트 배열을 numpy array로 변환 (OpenCV용)
        np_arr = np.frombuffer(image_bytes, np.uint8)

        # OpenCV 이미지 디코딩 (컬러 이미지)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # YOLO 모델에 이미지 넣고 탐지 수행
        results = model(img)

        # 탐지 결과를 JSON으로 보내기 위해 리스트 준비
        detections = []
        for *box, conf, cls in results.xyxy[0].tolist():
            detections.append({
                "bbox": box,                          # 바운딩 박스 좌표 [xmin, ymin, xmax, ymax]
                "confidence": round(conf, 2),        # 신뢰도 소수점 2자리까지
                "class_id": int(cls),                 # 클래스 ID (숫자)
                "class_name": model.model.names[int(cls)]  # 클래스 이름 (예: "person")
            })

        # 클라이언트에 "detection" 이벤트로 탐지 결과 전송
        emit("detection", detections)

    except Exception as e:
        # 예외 발생 시 에러 출력
        print("❌ YOLO 처리 중 에러:", e)


if __name__ == "__main__":
    # 서버 실행 (외부 접속 허용, 5000 포트, 디버그 모드 ON)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
