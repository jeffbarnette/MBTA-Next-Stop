// Create an API client
const apiClient = axios.create({
    baseURL: "http://127.0.0.1:5000",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json"
    }
});

function getRoutes() {
    // Get routes
    apiClient.get('/api/routes')
        .then(response => {
            var routes = response.data;
            document.getElementById('routes').innerHTML = "<option value=\"None\">Select a route..</option>";
            for (var key in routes) {
                document.getElementById('routes').innerHTML += "<option value=\"" + routes[key] + "\">" + key + "</option>";
            }
        })
        .catch(error => {
            console.log('There was an error:', error.response);
        });
}

function getStops() {
    // Get stops based on route selection
    var routeSelect = document.getElementById('routes');
    var route_id = routeSelect.options[routeSelect.selectedIndex].value;
    if (route_id !== 'None') {
        apiClient.get('/api/stops/' + route_id)
        .then(response => {
            var stops = response.data;
            document.getElementById('stops').innerHTML = "<option value=\"None\">Select a station..</option>";
            for (var key in stops) {
                document.getElementById('stops').innerHTML += "<option value=\"" + stops[key] + "\">" + key + "</option>";
            }
            document.getElementById('stops').disabled = false;
        })
        .catch(error => {
            console.log('There was an error:', error.response);
        });
    } else {
        document.getElementById('stops').innerHTML = "<option value=\"None\">Select a station..</option>";
        document.getElementById('stops').disabled = true;
        document.getElementById('directions').innerHTML = "<option value=\"None\">Select a route direction..</option>";
        document.getElementById('directions').disabled = true;
        document.getElementById('prediction').style.display = "none";
    }
}

function getDirections() {
    // Get route details based on route selection
    var routeSelect = document.getElementById('routes');
    var route_id = routeSelect.options[routeSelect.selectedIndex].value;
    var stopSelect = document.getElementById('stops');
    var stop_id = stopSelect.options[stopSelect.selectedIndex].value;
    if (route_id !== 'None' && stop_id !== 'None') {
        apiClient.get('/api/route/' + route_id)
        .then(response => {
            var routeDetails = response.data.data;
            var routeDirections = routeDetails.attributes['direction_names'];
            document.getElementById('directions').innerHTML = "<option value=\"None\">Select a route direction..</option>";
            for (var key in routeDirections) {
                document.getElementById('directions').innerHTML += "<option value=\"" + key + "\">" + routeDirections[key]
                + "</option>";
            }
            document.getElementById('directions').disabled = false;
        })
        .catch(error => {
            console.log('There was an error:', error.response);
        });
    } else {
        document.getElementById('directions').innerHTML = "<option value=\"None\">Select a route direction..</option>";
        document.getElementById('directions').disabled = true;
        document.getElementById('prediction').style.display = "none";
    }
}

function getPrediction() {
    // Get prediction
    var routeSelect = document.getElementById('routes');
    var route_id = routeSelect.options[routeSelect.selectedIndex].value;
    var stopSelect = document.getElementById('stops');
    var stop_id = stopSelect.options[stopSelect.selectedIndex].value;
    var stop_text = stopSelect.options[stopSelect.selectedIndex].text;
    var directionSelect = document.getElementById('directions');
    var direction_id = directionSelect.options[directionSelect.selectedIndex].value;
    var direction_text = directionSelect.options[directionSelect.selectedIndex].text;
    if (route_id !== 'None' && stop_id !== 'None' && direction_id !== 'None') {
        apiClient.get('/api/prediction/' + route_id + '/' + stop_id + '/' + direction_id)
        .then(response => {
            // Check if there is data in the response
            if (response.data.data.length > 0) {
                var predictions = response.data.data;
                var firstDepartTime = predictions[0].attributes['departure_time'];
                if (firstDepartTime != null) {
                    // Get the first available departing train
                    var departTime = new Date(firstDepartTime);
                    document.getElementById('prediction').innerHTML = "Next train heading " + direction_text.toLowerCase() + " departs at " + departTime;
                    document.getElementById('prediction').style.display = "block";
                } else {
                    // Double check for ANY departing trains at selected station heading in selected direction
                    for (i=0; i < predictions.length; i++) {
                        if (predictions[i].attributes['departure_time'] != null) {
                            firstDepartTime = predictions[i].attributes['departure_time'];
                            break;
                        }
                    }
                    // If there is a departing train, show it
                    if ( firstDepartTime != null) {
                        var departTime = new Date(firstDepartTime);
                        document.getElementById('prediction').innerHTML = "Next train heading " + direction_text.toLowerCase() + " departs at " + departTime;
                        document.getElementById('prediction').style.display = "block";
                    } else {
                        // No trains available
                        document.getElementById('prediction').innerHTML = "There are no trains scheduled to leave " 
                        + stop_text + " heading " + direction_text.toLowerCase();
                        document.getElementById('prediction').style.display = "block";
                    }
                }
            } else {
                // No trains available
                document.getElementById('prediction').innerHTML = "There are no trains scheduled to leave " 
                + stop_text + " heading " + direction_text.toLowerCase();
                document.getElementById('prediction').style.display = "block";
            }
        })
        .catch(error => {
            console.log('There was an error:', error.response);
        });
    } else {
        document.getElementById('prediction').style.display = "none";
    }
}

// Get routes on page load
getRoutes();