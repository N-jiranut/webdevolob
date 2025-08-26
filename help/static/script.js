document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send-btn");
  const input = document.getElementById("message-input");
  const chatBox = document.getElementById("chat-box");

  function addMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.textContent = text;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    // Show user message
    addMessage(message, "user");
    input.value = "";

    // Send to Flask
    const response = await fetch("/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();

    // Show bot reply
    addMessage(data.reply, "bot");
  }

  sendBtn.addEventListener("click", sendMessage);
  input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});
