from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
import os
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/detect', methods=['POST'])
def detect():
    print("Request content-type:", request.content_type)
    print("Request files:", request.files)
    print("Request form:", request.form)  
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 이미지 열기
    img = Image.open(filepath)

    # YOLOv5로 추론
    results = model(img)
    labels = results.xyxyn[0][:, -1].tolist()
    names = results.names
    detected = [names[int(i)] for i in labels]

    # 결과 정리
    result_count = {}
    for obj in detected:
        result_count[obj] = result_count.get(obj, 0) + 1

    summary = ', '.join([f"{k} {v}개" for k, v in result_count.items()])
    return jsonify({'result': summary or '감지된 객체 없음'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
