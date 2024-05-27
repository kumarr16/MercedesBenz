// Variables
const input = document.getElementById("question");
const dialog = document.getElementById('dialog');

// When the user presses enter.
input.addEventListener("keyup", function(event) {
  if (event.key === "Enter" && input.value) {
    userMessage();
    ajax();
  }
});

// New user message in the dialog box.
function userMessage() {
    /*
        <div class="message user">
            <p class="user">Question</p>
        </div>
    */
    let div = document.createElement('div');
    let p = document.createElement('p');

    div.classList.add('message', 'user');

    dialog.appendChild(div);
    div.appendChild(p);

    p.innerHTML = input.value;

    dialog.scrollTop = dialog.scrollHeight;
}

function ajax() {
    // Creation of the loader
    let div = document.createElement('div');
    div.classList.add('message', 'loader');
    dialog.appendChild(div);
    div.innerHTML = '<img src="static/loader.gif" width="32" height="32" alt="loader"/>';

    dialog.scrollTop = dialog.scrollHeight;

    // GET request
    var req = new XMLHttpRequest();
    req.open("GET", "/get?question=" + input.value);
    input.value = '';
    req.addEventListener("load", function () {
        var data = JSON.parse(req.responseText);
        div.classList.replace('loader', 'bot');

        if (data['status'] == "OK") {
            div.innerHTML = '<p>' + data['grandpy'] + '</p>';
            div.innerHTML += '<p><strong>' + data['formatted_address'] + '</strong></p>';
            div.innerHTML += '<p>' + data["summary"] + '</p>';
            div.innerHTML += '<p><a href="' + data["url"] + '">En savoir plus sur Wikipedia</a></p>';
            googleMap(data["lat"], data["lng"]);
        }

        if (data['status'] == "Place Error") {
            div.innerHTML = '<p>' + data['grandpy'] + '</p>';
        }

        if (data['status'] == "Map Error") {
            div.innerHTML = '<p>' + data['grandpy'] + '</p>';
        }

        dialog.scrollTop = dialog.scrollHeight;
    });
    req.send(null);
}

/***
    Google Maps API
***/
var map = {};
var marker = {};

// When the page is loaded shows the Eiffel Tower.
function initMap() {
    lat = 48.85837009999999;
    lng = 2.2944813;
    googleMap(lat, lng);
}

// Update the map.
function googleMap(latitude, longitude) {
    coordinates = {lat: latitude, lng: longitude};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: coordinates
    });
    marker = new google.maps.Marker({
        position: coordinates,
        map: map
    });
}
