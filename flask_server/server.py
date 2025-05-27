from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from PIL import Image
import io
import base64
import os

app = Flask(__name__)
CORS(app)

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=True)

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()
        image_data = data['image']

        # base64 디코딩 (prefix 없는 경우 바로 처리)
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))

        # YOLO 모델 예측
        results = model(image)

        # 결과 라벨 추출
        labels = results.pandas().xyxy[0]['name'].tolist()

        # 리스트 -> 문자열로 변환하여 전송
        return jsonify({"result": ", ".join(labels)})

    except Exception as e:
        print(f"오류 발생: {e}")
        return jsonify({"error": "객체 인식 중 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
