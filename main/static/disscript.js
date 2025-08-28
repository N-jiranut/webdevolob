// const socket = io('http://10.207.14.216:5000');
const socket = io('http://192.168.1.115:5000');
const chatBox = document.getElementById("dischat");
const input = document.getElementById("input-text");
const workbtn = document.getElementById("onworkBtn");
const delbtn = document.getElementById("delBtn");
const greenbtn = document.getElementById("green");
// greenbtn.style.backgroundColor = "rgb(2, 255, 35)"
const redbtn = document.getElementById("red");
function sendMessage(){
    const text = input.value
    if (text.trim() !== "") {
        socket.emit("mainmessage", text, "ipad");
    }
    chatBox.scrollTop = chatBox.scrollHeight;
    input.value = "";
    input.focus();
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
  const sendBtn = document.getElementById("sendBtn");

  // กดปุ่ม Send
  sendBtn.addEventListener("click", sendMessage);
  delbtn.addEventListener("click", function() {
    input.value="";
  });
  workbtn.addEventListener("click", function(){
    socket.emit("work")
  });

  // กด Enter
  input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
});
