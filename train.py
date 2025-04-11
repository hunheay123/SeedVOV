from ultralytics import YOLO

# 1. 모델 불러오기 (기존 모델 or 새로 학습할 모델)
model = YOLO("yolov8n.yaml")  # 처음부터 학습할 거면 .yaml 사용
# 또는 사전학습된 걸 fine-tune 할 거면
# model = YOLO("yolov8n.pt") 

# 2. 학습 시작
model.train(
    data="d:/VoV/my-yolo/data.yaml",     # 클래스 이름과 경로를 정의한 yaml 파일
    epochs=50,            # 학습 횟수
    imgsz=640,            # 이미지 크기
    batch=8,              # 배치 사이즈 (메모리에 따라 조절)
    project="runs/train", # 결과 저장 폴더
    name="custom_yolo"    # 결과 하위 폴더 이름
)
