const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  const msgElem = document.createElement('div');
  msgElem.className = 'message';
  msgElem.textContent = text;
  chatMessages.appendChild(msgElem);

  maybeAutoScroll();
  chatInput.value = '';
}

function isUserAtBottom() {
  // Checks if user is near the bottom of chat
  return chatMessages.scrollTop + chatMessages.clientHeight >= chatMessages.scrollHeight - 10;
}

function maybeAutoScroll() {
  if (isUserAtBottom()) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});
