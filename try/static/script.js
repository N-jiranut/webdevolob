// document.addEventListener("DOMContentLoaded", () => {
//     const socket = io();

//     const chatBox = document.getElementById("chatbox");
//     const Input = document.getElementById("message");
//     const button = document.getElementById("button")

    // socket.on("message", function(msg) {
    //     let p = document.createElement("p");
    //     chatBox.appendChild(p);
    //     chatBox.scrollTop = chatBox.scrollHeight;
    //     p.textContent = msg;
    // });

//     button.addEventListener('click', function() {
//         document.getElementById("test").textContent = "working";
//     });
// });

const socket = io();
// document.addEventListener("DOMContentLoaded", () => {
const chatBox = document.getElementById("chatbox");

socket.on("message", function(msg) {
    let p = document.createElement("p");
    p.textContent = msg;
    chatBox.appendChild(p);
    chatBox.scrollTop = chatBox.scrollHeight;
});

button.addEventListener('click', function() {
    const text = document.getElementById("why").value
    if (text.trim() !== "") {
        socket.emit("don", text);
    }
    document.getElementById("why").value = "";
});

socket.on("don", function(msg) {
        let p = document.createElement("p");
        p.textContent = msg;
        chatBox.appendChild(p);
        // chatBox.scrollTop = chatBox.scrollHeight;
    });

// });