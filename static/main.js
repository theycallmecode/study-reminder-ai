function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value;
    if (!message) return;

    const chatBox = document.getElementById('chat-box');
    const userMsg = document.createElement('p');
    userMsg.innerHTML = `<strong>You:</strong> ${message}`;
    userMsg.classList.add('fade-in');
    chatBox.appendChild(userMsg);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const aiMsg = document.createElement('p');
        aiMsg.innerHTML = `<strong>AI:</strong> ${data.response}`;
        aiMsg.classList.add('fade-in');
        chatBox.appendChild(aiMsg);
        chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
    });

    input.value = '';
}

function setReminder() {
    const taskInput = document.getElementById('reminder-task');
    const timeInput = document.getElementById('reminder-time');
    const task = taskInput.value;
    const time = timeInput.value;

    if (!task || !time) {
        alert('Designate both a task and a temporal coordinate!');
        return;
    }

    const chatBox = document.getElementById('chat-box');
    const userMsg = document.createElement('p');
    userMsg.innerHTML = `<strong>You:</strong> Set reminder: ${task} at ${time}`;
    userMsg.classList.add('fade-in');
    chatBox.appendChild(userMsg);
    chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });

    fetch('/set_reminder', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task: task, time: time })
    })
    .then(response => response.json())
    .then(data => {
        const aiMsg = document.createElement('p');
        aiMsg.innerHTML = `<strong>AI:</strong> ${data.response}`;
        aiMsg.classList.add('fade-in');
        chatBox.appendChild(aiMsg);
        chatBox.scrollTo({ top: chatBox.scrollHeight, behavior: 'smooth' });
    });

    taskInput.value = '';
    timeInput.value = '';
}