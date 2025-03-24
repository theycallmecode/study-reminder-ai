function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value;
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    
    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    input.value = '';
}