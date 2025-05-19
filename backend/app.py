from flask import Flask, request, jsonify, render_template
import torch
import cv2
import numpy as np
from PIL import Image

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Flask 서버 초기화
app = Flask(__name__)

# 🔹 웹 UI 렌더링 (웹캠 활성화 포함)
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    # 이미지 받기
    image_file = request.files['image']
    image = Image.open(image_file)

    # YOLOv5로 객체 탐지 수행
    results = model(image)

    # 탐지된 객체 정보 추출
    objects = []
    for *box, conf, cls in results.xyxy[0].tolist():
        objects.append({
            "bbox": box,
            "confidence": conf,
            "class": int(cls)
        })

    return jsonify({'detections': objects})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)