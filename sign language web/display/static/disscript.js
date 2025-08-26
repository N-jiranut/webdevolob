// function initCamera() {
//   const video = document.getElementById('video');
//   navigator.mediaDevices.getUserMedia({ video: true, audio: false })
//     .then(stream => { video.srcObject = stream; })
//     .catch(err => { console.error("Camera error:", err); });
// }

function sendMessage() {
  const input = document.getElementById("input-text");
  const message = input.value.trim();
  if (message === "") return;

  const chatBox = document.getElementById("dischat");  // กล่องแชทหลัก (ด้านขวา)

  // ✅ แสดงข้อความฝั่งเรา
  const msgDiv = document.createElement("div");
  msgDiv.className = "message right";
  msgDiv.innerHTML = `
    <div class="msg-bubble self">${message}</div>
    <div class="circle"></div>
  `;
  chatBox.appendChild(msgDiv);

  // scroll ลงล่างอัตโนมัติ
  chatBox.scrollTop = chatBox.scrollHeight;

  localStorage.setItem("chatMessage", JSON.stringify({ sender: "dischat", text: message }));
  
  // reset input
  input.value = "";
  input.focus();
}

// ✅ รอ DOM โหลดเสร็จแล้วค่อย bind event
document.addEventListener("DOMContentLoaded", () => {
  // initCamera();

  const input = document.getElementById("input-text");
  const sendBtn = document.getElementById("sendBtn");

  // กดปุ่ม Send
  sendBtn.addEventListener("click", sendMessage);

  // กด Enter
  input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
});
