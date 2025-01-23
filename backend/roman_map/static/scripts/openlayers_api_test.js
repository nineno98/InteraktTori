
const map = new ol.Map({
    target: 'map',
    layers: [
        new ol.layer.Tile({
            source: new ol.source.OSM() 
        })
    ],
    view: new ol.View({
        center: ol.proj.fromLonLat([0, 0]), 
        zoom: 2
    })
});


const vectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://127.0.0.1:8000/territories/' 
});

const styleFunction = (feature) => {
    
    let color = ol.color.asArray(feature.get('color')).slice();
    color[3] = 0.5;
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'black', 
            width: 2
        }),
        fill: new ol.style.Fill({
            color: color 
        })
    });
};


const vectorLayer = new ol.layer.Vector({
    source: vectorSource,
    style: styleFunction,
    
});


map.addLayer(vectorLayer);
