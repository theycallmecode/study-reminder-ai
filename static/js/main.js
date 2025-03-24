function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value;
    if (!message) return;

    const output = document.getElementById('chat-output');
    output.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        output.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
        output.scrollTop = output.scrollHeight;
    });

    input.value = '';
}

function setReminder() {
    const time = document.getElementById('reminder-time').value;
    const task = document.getElementById('reminder-task').value;
    if (!time || !task) return;

    fetch('/set_reminder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ time: time, task: task })
    })
    .then(response => response.json())
    .then(data => alert(data.status));

    document.getElementById('reminder-task').value = '';
}