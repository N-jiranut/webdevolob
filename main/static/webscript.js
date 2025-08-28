// const input = document.getElementById("input-text");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("webchat");
const input = document.getElementById("input-text");
const socket = io('http://10.207.14.216:5000');

// function sendMessage() {
//   const message = input.value.trim();
//   if (message === "") return;

//   // ✅ กล่องข้อความ (ฝั่งเรา)
//   const msgDiv = document.createElement("div");
//   msgDiv.classList.add("message", "right"); // right = ฝั่งเรา
//   msgDiv.innerHTML = `
//     <div class="msg-bubble self">${message}</div>
//     <div class="circle"></div>
//   `;
//   chatBox.appendChild(msgDiv);

//   // ✅ scroll ลงล่างอัตโนมัติ
//   chatBox.scrollTop = chatBox.scrollHeight;

//   // ✅ clear input
//   input.value = "";
//   input.focus();
// }

function sendMessage(){
    const text = document.getElementById("input-text").value
    if (text.trim() !== "") {
        socket.emit("mainmessage", text, "laptop");
    }
    chatBox.scrollTop = chatBox.scrollHeight;
    document.getElementById("input-text").value = "";
    input.focus();
}
socket.on("take", function(msg, user) {
  if (user=="laptop"){side="right";}else{side="left";}

  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", side);
  msgDiv.innerHTML = `<div class="msg-bubble">${msg}</div>`;
  chatBox.appendChild(msgDiv);
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
