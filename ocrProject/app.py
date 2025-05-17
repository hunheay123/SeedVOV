# app.py (Flask 서버)
from flask import Flask, request, jsonify
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['ko', 'en'])

@app.route('/ocr', methods=['POST'])
def ocr():
    image = request.files['image']
    image.save("temp.jpg")
    result = reader.readtext("temp.jpg")
    text = ' '.join([res[1] for res in result])
    os.remove("temp.jpg")
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)