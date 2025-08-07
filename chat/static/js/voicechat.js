let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
let ws_url = ws_scheme + "://" + window.location.host + "/ws/voicechat/";
let ws = new WebSocket(ws_url);

let audioChunks = [];
let mediaRecorder = null;
let mediaStream = null;

const recBtn = document.getElementById('recBtn');
const chatlog = document.getElementById('chatlog');
const audioPlayer = document.getElementById('audioPlayer');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);

    // 텍스트 채팅 표시
    if (data.prompt) {
        chatlog.innerHTML += `<li><b>Q:</b> ${data.prompt}</li>`;
    }
    if (data.response) {
        chatlog.innerHTML += `<li><b>A:</b> ${data.response}</li>`;
    }
    // 음성 답변 재생
    if (data.audio_base64) {
        audioPlayer.src = "data:audio/mp3;base64," + data.audio_base64;
        audioPlayer.play();
    }
};

recBtn.onclick = async function() {
    if (!mediaRecorder) {
        // 마이크 허용 및 녹음 시작
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(mediaStream, { mimeType: 'audio/webm' }); // mp3 지원 브라우저만 type='audio/mp3'
        audioChunks = [];

        mediaRecorder.ondataavailable = function(e) {
            if (e.data.size > 0) audioChunks.push(e.data);
        };
        mediaRecorder.onstop = function() {
            // 녹음 끝난 후 서버로 데이터 전송
            let blob = new Blob(audioChunks, { type: 'audio/webm' });
            audioChunks = [];

            // 1. 녹음 파일을 브라우저에서 재생
            const recordedUrl = URL.createObjectURL(blob);
            audioPlayer.src = recordedUrl;
            audioPlayer.play();

            // 2. 서버로 전송
            blob.arrayBuffer().then(buffer => {
                ws.send(buffer);
            });

            // 마이크 해제
            mediaStream.getTracks().forEach(track => track.stop());
            mediaRecorder = null;
            recBtn.textContent = "녹음 시작";
        };
        mediaRecorder.start();
        recBtn.textContent = "녹음 중지";
    } else {
        mediaRecorder.stop();
    }
};
