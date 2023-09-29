var elevation = {};
load_elevation();

function load_elevation(){
    console.log(tid);
    fetch("/elevation?id="+tid, {
        method: "GET",
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
    })
    .then(res => res.json())
    .then(res => {
        elevation = res;
    })
    .finally(() => {
        drawElevationGraph();
    });
}

function drawElevationGraph(){
    var ctx = document.getElementById('elevationChart').getContext('2d');
    
    var data = {
        labels: Object.keys(elevation),
        datasets: [{
            label: 'Erhöhung',
            data: Object.values(elevation),
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };
    
    new Chart(ctx, {
        type: 'line',
        data: data
    });

}
