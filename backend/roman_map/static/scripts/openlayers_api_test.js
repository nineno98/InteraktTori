// Alaptérkép létrehozása
const map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM() // Alaptérkép (OpenStreetMap)
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([0, 0]), // Alapértelmezett középpont
        zoom: 2
    })
});

// GeoJSON réteg létrehozása
const vectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://127.0.0.1:8000/territories/' // API végpont
});

const styleFunction = (feature) => {
    
    let color = ol.color.asArray(feature.get('color')).slice();
    color[3] = 0.5;
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'black', // Körvonal színe
            width: 2
        }),
        fill: new ol.style.Fill({
            color: color // Feature saját színe
        })
    });
};

// Stílus a MultiPolygonokhoz
const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: styleFunction,
    
});

// Réteg hozzáadása a térképhez
map.addLayer(vectorLayer);
