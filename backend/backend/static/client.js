const video = document.getElementById("video");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const socket = io();

// 웹캠 시작
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    });

    function sendFrame() {
        const tempCanvas = document.createElement("canvas");
        const tempCtx = tempCanvas.getContext("2d");

        tempCanvas.width = video.videoWidth;
        tempCanvas.height = video.videoHeight;

        tempCtx.drawImage(video, 0, 0);  // 비디오 프레임을 임시 캔버스에 그림
        const imageData = tempCanvas.toDataURL("image/jpeg");  // 여기 tempCanvas에서 이미지 가져와야 함
        const data = {
            image: imageData
        };
        socket.emit("image", JSON.stringify(data));
    }


socket.on("detection", (data) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    data.forEach((obj) => {
        const [x1, y1, x2, y2] = obj.bbox;
        const label = `${obj.class_name}: ${obj.confidence.toFixed(2)}`;

        ctx.strokeStyle = "lime";
        ctx.lineWidth = 2;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        ctx.fillStyle = "lime";
        ctx.font = "16px sans-serif";
        ctx.fillText(label, x1 + 4, y1 - 4);
    });

    // 다시 다음 프레임 보내기
    setTimeout(sendFrame, 1000); // 0.2초마다 요청
});

video.addEventListener("play", () => {
    sendFrame();
});
