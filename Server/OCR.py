from flask import Flask, request, jsonify
import numpy as np
import cv2
import easyocr

app = Flask(__name__)
reader = easyocr.Reader(['ko', 'en'], gpu=False)

# 전처리 함수인데 현재는 사용은 하지 않음. 나중에 필요하면 사용예정
# 참고로 이 함수는 잘 작동하는지 모르겠음... 실행해본적이 없어서...
def preprocess_image(image_path):
    """이미지를 불러와서 그레이스케일 + 이진화 처리"""
    image = cv2.imread(image_path)

    # 1. 그레이스케일 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. 대비 향상 (히스토그램 평활화)
    gray = cv2.equalizeHist(gray)

    # 3. 가우시안 블러로 노이즈 제거 (옵션)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # 4. Adaptive Threshold 이진화
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # or ADAPTIVE_THRESH_MEAN_C
        cv2.THRESH_BINARY,
        31,   # blockSize (홀수, 보통 11~51 사이)
        5     # C값 (조정 가능)
    )

    return thresh

@app.route('/ocr/image', methods=['POST'])
def ocr():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    results = reader.readtext(image)

    text = "\n".join([res[1] for res in results])
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
