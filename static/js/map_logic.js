var map = L.map('map').setView([50.087, 10.516], 6);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var activeLines = {};
var searchForm = false;
var nicknames = [];
var vehicles = [];
load_user_nicknames();
load_vehicles();

function toggle_track(track){
    const pattern = /\((.*)\)/;
    const matches = track.match(pattern);
    track = matches[1].split(",");

    if(activeLines[track[0]] === undefined){
        load_path(track);
    }else{
        remove_path(track);
    }
}

document.getElementById('import-button').addEventListener('click', function(event){
    event.preventDefault();
    window.location.href = "/import_files";
});

function load_path(track){
    fetch("/draw_path", {
        method: "POST",
        body: JSON.stringify({
          tid: track[0],
          dateiname: track[1],
          fzid: track[3]
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(res => res.json())
    .then(res => {
        var polyline = L.polyline(res, {color: 'red'}).addTo(map);
        map.fitBounds(polyline.getBounds());
        activeLines[track[0]] = polyline;
    });
}

function remove_path(track){
    map.removeLayer(activeLines[track[0]]);
    delete activeLines[track[0]];
}

function load_user_nicknames(){
    fetch("/nicknames", {
        method: "GET",
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(res => res.json())
    .then(res => {
        nicknames = res;
    });
}

function load_vehicles(){
    fetch("/vehicles", {
        method: "GET",
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(res => res.json())
    .then(res => {
        vehicles = res;
    });
}

function submitSearchForm(){
    document.getElementById('search').submit();
}

function toggleSearchForm(){
    if(searchForm){
        document.getElementById("searchForm").outerHTML = "";
        searchForm = false;
    }else{
        var div = document.createElement('div');
        div.className = "search-form";
        div.id = "searchForm";

        div.innerHTML = `
        <div class="nav-button" onclick="toggleSearchForm()">
            Karte ...
        </div>
        <div class="nav-button" onclick="submitSearchForm()">
            Suchen
        </div>
        <form id="search" action="/search" method="post">
        <label for="user">Fahrerkürzel:</label>
        <select id="user" type="text" name="user"></select><br>
        <label for="vehicle">Fahrzeug:</label>
        <select id="vehicle" type="text" name="vehicle"></select><br>
        <label for="start-time">Von:</label>
        <input type="datetime-local" id="start-time" name="start-time"><br>
        <label for="start-time">Bis:</label>
        <input type="datetime-local" id="end-time" name="end-time"><br>
        </form>
        `;

        document.getElementById("anchor").appendChild(div);
        
        html = "<option></option>";
        for(var key in nicknames){
            html += "<option value=" + nicknames[key] + ">" + nicknames[key] + "</option>";
        }
        document.getElementById('user').innerHTML = html;

        html = "<option></option>";
        for(var key in vehicles){
            html += "<option value=" + vehicles[key] + ">" + vehicles[key] + "</option>";
        }
        document.getElementById('vehicle').innerHTML = html;

        searchForm = true;
    }
}