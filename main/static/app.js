
var map;
var layer;
var geocoder;
var api_version = 1;

function initMap() {
    var initLatLng = {lat: 40.873, lng: 13.907};

    // Create the geocoder: used to lookup address given lat/lon
    geocoder = new google.maps.Geocoder();

    // Create the map object
    map = new google.maps.Map(document.getElementById('map'), {
      center: initLatLng,
      zoom: 8
    });

    // Add click event listener
    map.addListener('click', function(e) {mapClick(e);});

    // Create the Fusion Table layer on the map: reflects all the location data from the table on the map
    // NB: the where clause is always true and is a hack to invalidate the cache
    layer = new google.maps.FusionTablesLayer({
        query: {
                select: 'Location',
                from: fusion_table_id,
                where: "Location NOT EQUAL TO '"+new Date().getTime()+"'"
              },
        map: map
    });
}

function mapClick(event) {
    // lookup the location address given the event.latLng and add it if valid
    geocoder.geocode({'location': event.latLng}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results.length >= 1) {
                var location_type = results[0].geometry.location_type;
                if (location_type == 'ROOFTOP' || location_type == 'GEOMETRIC_CENTER') {
                    // it is a valid location
                    var coord = results[0].geometry.location;
                    var address = results[0].formatted_address;
                    var location = {lat: coord.lat(), lng: coord.lng(), address: address};
                    addAddress(location);
                }
            }
        }
    });
}

function addAddress(location){
    // send the location to the backend to add to the db and fustion table in case it's not a duplicate
    $.ajax({
        type: "POST",
        dataType: 'json',
        url: 'api/'+api_version+'/locations/add',
        data: {
            lat: location.lat,
            lng: location.lng,
            address: location.address,
            csrfmiddlewaretoken: csrftoken,
          },
        success: function (data) {
            if (data.result === 'ok'){
                // add to the list of addresses
                $('#locations').append('<li>'+ location.address + '</li>');

                // update the map
                refreshLayer();
            } else {
                alert(data.result);
            }
        }
    });
}

function removeAll(){
    // clean the db, the map and the list of addresses
    $.ajax({
        type: "POST",
        dataType: 'json',
        url: 'api/'+api_version+'/locations/removeall',
        data: {csrfmiddlewaretoken: csrftoken},
        success: function (data){
            if (data.result === 'ok'){
                // clean the list of addresses
                $('#locations').empty();

                // update the map
                refreshLayer();
            } else {
                alert(data.result);
            }
        }
    });
}

function refreshLayer() {
    // hack to force a cache update of the map tiles
    layer.setOptions({
        query: {
            select: 'Location',
            from: fusion_table_id,
            where: "Location NOT EQUAL TO '"+new Date().getTime()+"'"
        }
    });
}
