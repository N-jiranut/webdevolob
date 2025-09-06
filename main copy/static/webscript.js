const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("webchat");
const input = document.getElementById("input-text");
// const socket = io('http://10.207.14.79:5000');
const socket = io('http://192.168.1.115:5000');

function sendMessage(){
    const text = input.value
    input.value = "";
    if (text.trim() !== "") {
        socket.emit("laptopmessage", text);
    }
    input.focus();
}
socket.on("take", function(msg, user) {
  if (user=="laptop"){side="right";}else{side="left";}

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", side);
  msgDiv.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
});

// ปุ่ม Send
sendBtn.addEventListener("click", sendMessage);

// ปุ่ม Enter
input.addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});
