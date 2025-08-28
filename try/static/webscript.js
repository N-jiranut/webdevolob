const input = document.getElementById("input-text");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("webchat");
const socket = io('http://10.207.14.216:5000');
let side = "right";

socket.on("take", function(msg, user) {
  if (user=="laptop"){side="right";}else{side="left";}
  document.getElementById("fortest").textContent=user

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", side);
  msgDiv.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
});

function sendMessage(){
  const text = input.value
  if (text.trim() !== "") {
      socket.emit("mainmessage", text, "laptop");
  }
  input.value = "";
}


sendBtn.addEventListener("click", sendMessage);

// ปุ่ม Enter
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
