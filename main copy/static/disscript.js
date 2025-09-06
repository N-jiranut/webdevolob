// const socket = io('http://10.207.14.79:5000');
const socket = io('http://192.168.1.115:5000');

const chatBox = document.getElementById("dischat");
const input = document.getElementById("input-text")
const workbtn = document.getElementById("onworkBtn");
const delbtn = document.getElementById("delBtn");
const greenbtn = document.getElementById("green");
// greenbtn.style.backgroundColor = "rgb(2, 255, 35)"
const redbtn = document.getElementById("red");
function sendMessage(){
  greenbtn.style.backgroundColor = "rgba(20, 129, 16, 1)";
  socket.emit("dismessage", input.value);
}

socket.on("add_text", function(label){
  let newtext = input.value + " " + label
  input.value = newtext;
});

socket.on("take", function(msg, user) {
  input.value=""
  if (user=="laptop"){side="right";}else{side="left";}

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", side);
  msgDiv.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on("redlighton", function(){
  redbtn.style.backgroundColor = "rgba(247, 38, 38, 1)";
});
socket.on("next", function(){
  redbtn.style.backgroundColor = "rgba(100, 10, 10, 1)";
  greenbtn.style.backgroundColor = "rgba(47, 255, 40, 1)";
});
socket.on("addonbtn", function(){
  sendMessage()
});

// ✅ รอ DOM โหลดเสร็จแล้วค่อย bind event
document.addEventListener("DOMContentLoaded", () => {
  // initCamera();
  const sendBtn = document.getElementById("sendBtn");

  // กดปุ่ม Send
  sendBtn.addEventListener("click", sendMessage);

  delbtn.addEventListener("click", function() {
    greenbtn.style.backgroundColor = "rgba(20, 129, 16, 1)";
    socket.emit("fordelete");
  });

  workbtn.addEventListener("click", function(){
    socket.emit("work");
  });
});
