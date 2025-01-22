window.onload = init;

function init() {
    let map = new ol.Map({
        target: "map",
        view: new ol.View({
            center: ol.proj.fromLonLat([72.88, 19.12]),  // Mumbai középpontja
            zoom: 11,
            maxZoom: 20,
            minZoom: 5
        })
    });

    const openStreetMapStandard = new ol.layer.Tile({
        source: new ol.source.OSM(),
        visible: true,
        title: "OSM_Standard"
    });

    map.addLayer(openStreetMapStandard);

    // Mumbai MultiPolygon koordináták (EPSG:4326-ból EPSG:3857-be konvertálva)
    const multiPolygonCoords = [
        [
            [72.775, 19.260],
            [72.995, 19.260],
            [72.995, 19.100],
            [72.775, 19.100],
            [72.775, 19.260]
        ],
        [
            [72.830, 19.230],
            [73.050, 19.230],
            [73.050, 19.070],
            [72.830, 19.070],
            [72.830, 19.230]
        ]
    ];

    // A koordináták konvertálása EPSG:4326-ról EPSG:3857-re
    const multiPolygon = new ol.Feature({
        geometry: new ol.geom.MultiPolygon(
            multiPolygonCoords.map(polygon => 
                polygon.map(coord => ol.proj.fromLonLat(coord))
            )
        )
    });

    // Stílus beállítása
    multiPolygon.setStyle(new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.3)'
        })
    }));

    const vectorSource = new ol.source.Vector({
        features: [multiPolygon]
    });

    const vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });

    map.addLayer(vectorLayer);
}
