const socket = io('http://10.207.14.216:5000');
const chatBox = document.getElementById("dischat");
function sendMessage(){
    const text = document.getElementById("input-text").value
    if (text.trim() !== "") {
        socket.emit("mainmessage", text, "ipad");
    }
    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById("why").value = "";
    input.focus();
    document.getElementById("input-text")=""
}
socket.on("take", function(msg, user) {
  if (user=="laptop"){side="right";}else{side="left";}

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", side);
  msgDiv.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  chatBox.appendChild(msgDiv);
});

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
