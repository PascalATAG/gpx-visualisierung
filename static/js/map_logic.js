var activeLines = {};

function load_path(track){
    const pattern = /\((.*)\)/;
    const matches = track.match(pattern);
    track = matches[1].split(",");
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