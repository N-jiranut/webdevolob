const input = document.getElementById("input-text");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("webchat");

function sendMessage() {
  const message = input.value.trim();
  if (message === "") return;

  // ✅ กล่องข้อความ (ฝั่งเรา)
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", "right"); // right = ฝั่งเรา
  msgDiv.innerHTML = `
    <div class="msg-bubble self">${message}</div>
    <div class="circle"></div>
  `;
  chatBox.appendChild(msgDiv);

  // ✅ scroll ลงล่างอัตโนมัติ
  chatBox.scrollTop = chatBox.scrollHeight;

  // ✅ clear input
  input.value = "";
  input.focus();
}

// ปุ่ม Send
sendBtn.addEventListener("click", sendMessage);

// ปุ่ม Enter
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
