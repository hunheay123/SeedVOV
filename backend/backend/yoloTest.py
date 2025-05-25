import torch
import cv2

def main():
    # YOLOv5 모델 로드 (처음에만 로드)
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", force_reload=False)
    model.eval()

    # 테스트할 이미지 경로
    image_path = "test1.jpg"  # 이미지 파일명/경로 적당히 바꿔 써

    # 이미지 읽기 (OpenCV)
    img = cv2.imread(image_path)
    if img is None:
        print(f"이미지 파일을 찾을 수 없습니다: {image_path}")
        return

    # BGR → RGB 변환
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 모델에 RGB 이미지 넣기
    results = model(img_rgb)

    # 결과 콘솔 출력
    results.print()

    # 결과 이미지 창으로 보여주기 (박스 포함)
    results.show()

if __name__ == "__main__":
    main()
