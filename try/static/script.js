const socket = io('http://10.207.14.216:5000');
const chatBox = document.getElementById("chatbox");

socket.on("take", function(msg) {
    let p = document.createElement("p");
    p.textContent = msg;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
});

function sendMessage(){
    const text = document.getElementById("why").value
    if (text.trim() !== "") {
        socket.emit("mainmessage", text, "ipad");
    }
    document.getElementById("why").value = "";
}

button.addEventListener('click', sendMessage);