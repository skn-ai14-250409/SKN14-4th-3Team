const socket = new WebSocket('ws://localhost:8000/ws/chat/');

socket.onopen = function(e) {
    socket.send(JSON.stringify({'message': 'Hello, WebSocket!'}));
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('서버에서 받은 메시지:', data.message);
};