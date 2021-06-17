var user = user;
var loc = window.location;
console.log(loc);

var ws = "ws:"
if (loc.protocol == "https") ws = "wss:"

var url = `${ws}//${loc.host}${loc.pathname}`;
console.log(url);

var socket = new WebSocket(url);

socket.onopen = function(event){
    console.log(event)
    var form = document.getElementById("msg-form");
    form.addEventListener("submit", (event) => {
        event.preventDefault();
        var inp = document.getElementById("msg-input");
        var value = inp.value;
        console.log(value);
        var data = {
            "user": user,
            "message": value,
        }
        socket.send(data=JSON.stringify(data))
    });
};

socket.onmessage = function(event){
    console.log(event)
};

socket.onerror = function(event){
    console.log(event)
};

socket.onclose = function(event){
    console.log(event)
};
