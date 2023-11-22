const videoFrame = document.getElementById('videoFrame');
let ws;

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = function(event) {
        console.log("WebSocket is open now.");
    };

    ws.onmessage = function(event) {
        videoFrame.src = 'data:image/jpeg;base64,' + event.data;
    };

    ws.onerror = function(event) {
        console.error("WebSocket error observed:", event);
    };

    ws.onclose = function(event) {
        console.log("WebSocket is closed. Reconnecting in 3 seconds...");
        setTimeout(connectWebSocket, 3000); // Attempt to reconnect after 3 seconds
    };
}

connectWebSocket(); // Initial WebSocket connection

// Optionally, you can add a button to manually trigger reconnection

