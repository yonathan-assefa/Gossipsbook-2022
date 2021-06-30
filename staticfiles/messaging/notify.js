function listenToSocket(){

    var user = user;
    const csrfToken = csrf_token;
    var loc = window.location;
    console.log(loc);

    var ws = "ws:"
    if (loc.protocol == "https") ws = "wss:"

    var url = `${ws}//${loc.host}/notifications/`;
    console.log(url);

    var socket = new WebSocket(url);

    socket.onopen = function(event){
        console.log(event)
        var form = document.getElementsByTagName("form")[0];
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            fetch('/notifications/room/', {
                "method": "POST",
                "headers": {
                    "X-CSRFToken": csrfToken
                }
            });
        })
    };

    socket.onmessage = function(event){
        console.log(event);
        var data = event["data"]

        var notificationListDiv = document.getElementById("notification-list");
        var div = document.createElement('div');
        div.classList.add("card");
        
        div.innerHTML = `
        <div class="card-body">
            <p class="card-text">${data}</p>
        </div>
        `;

        notificationListDiv.appendChild(div);
    };

    socket.onerror = function(event){
        console.log(event)
    };

    socket.onclose = function(event){
        console.log(event)
    };

};


listenToSocket();
