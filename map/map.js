/*
    Dark map: https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png
        Attrib: Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.
    Default map: https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
        Attrib: Map data &copy; OpenStreetMap contributors
*/
var map = L.map('map', {
    'center': [0,0],
    'zoom': 2,
    'layers': [
        L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png', {
        'attribution': 'Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'})
    ]
});
map.fitWorld().zoomIn();

function popupbox(feature, layer) {
    if (feature.properties) {
        var out = [];
        for(key in feature.properties) {
            out.push("<strong>"+key+":</strong> "+feature.properties[key]);
        }

        layer.bindPopup(out.join("<br>"));
    }
}
function customStyle(feature) {
    return {fillColor: feature.properties.color};
}
function createCircleMarker( feature, latlng ){
    // Change the values of these options to change the symbol's appearance
    let options = {
        radius: 4,
        fillColor: "lightgreen",
        color: "black",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
    }
    return L.circleMarker( latlng, options );
}

$.getJSON('data.geo.json', function (geojson) {
    L.geoJson(geojson,
    {
        onEachFeature: popupbox,
        pointToLayer: createCircleMarker,
        style: customStyle
    }).addTo(map);
});
