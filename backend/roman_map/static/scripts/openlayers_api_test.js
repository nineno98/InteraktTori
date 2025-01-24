
class RotateNorthControl extends ol.control.Control {
    /**
     * @param {Object} [opt_options] Control options.
     */
    
    constructor(opt_options) {
    const options = opt_options || {};
    const element = document.createElement('div');
    element.className = 'rotate-north ol-unselectable ol-control';
    super({
        element: element,
        target: options.target,
    });
        this.state = 0;
        this.button = document.createElement('button');
        this.button.innerHTML = 'N';
        element.appendChild(this.button);

        this.button.addEventListener('click', this.showOrHiddePolygons ,false );
    }
    testFunc = () => {
        console.log('testing');
    }
    showOrHiddePolygons = () => {
        if(this.state == 1){ // 0 rejtés, 1 mutat
            this.button.style.background = 'white';
            this.state = 0;
            //console.log(this.state)
            customPolygonsVectorLayer.setVisible(false);
        }else{
            this.button.style.background = 'lightgrey';
            this.state = 1;
            //console.log(this.state)
            customPolygonsVectorLayer.setVisible(true);
        }
    }
};



const map = new ol.Map({
    controls: ol.control.defaults.defaults({
        zoom : true,
    }).extend([new RotateNorthControl()]),
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
    color[3] = 0.0;
    let strokeColor = 'rgba(0, 0, 0, 0.0)'
    if(feature.get('hidden')){
        color[3] = 0.5;
        strokeColor = 'rgba(0, 0, 0, 1)'
    }
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: strokeColor, 
            width: 1
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


function filterByDate(selectedDate){
    document.getElementById('slider-value').textContent = selectedDate;

    vectorSource.forEachFeature((feature) => {
        let stard_date = feature.get('start_date')
        let end_date = feature.get('end_date')
        if(selectedDate < stard_date || selectedDate >= end_date){
            feature.set('hidden', false);
        }else{
            feature.set('hidden', true);
        }

        feature.changed()
    })
}
document.getElementById('date-slider').addEventListener('input', function (event){
    let selectedDate = parseInt(event.target.value)
    filterByDate(selectedDate);   
});

// selecting

function capitalizeFirstCharacters(value){
    return String(value).charAt(0).toUpperCase() + String(value).slice(1);
}

function handleDates(value){
    let number = parseInt(value);
    if(!isNaN(number)){     
        if(number <= 0){
            return 'Kr. e. '+String(Math.abs(number));
        }
        else{
            return 'Kr. u. '+String(number);
        }
    }
    else{
        return value
    }
}

let select = null;
function selectStyle(feature) {
    let color = ol.color.asArray(feature.get('color')).slice();
    color[3] = 0.0;
    let strokeColor = 'rgba(0, 0, 0, 0.0)';

    let featureName = capitalizeFirstCharacters(feature.get('name')) || 'N/A';
    let start_date = handleDates(feature.get('start_date') || 'N/A');
    let end_date = handleDates(feature.get('end_date') || 'N/A');


    if(feature.get('hidden')){
        color[3] = 0.5;
        strokeColor = 'rgba(255, 255, 255, 0.7)'
    }
    return new ol.style.Style({
        fill: new ol.style.Fill({
            color: color, 
        }),
        stroke: new ol.style.Stroke({
            color: strokeColor,
            width: 2,
        }),
        text: new ol.style.Text({
            font: '14px Arial',
            fill: new ol.style.Fill({ color: '#000' }),
            stroke: new ol.style.Stroke({ color: '#fff', width: 2 }),
            text: `${featureName}\n${start_date} - ${end_date}`,
            offsetY: -10,
        }),
    });
}

const selectSingleClick = new ol.interaction.Select({
    style: selectStyle,
});

function changeInteraction() {
    if (select !== null) {
        map.removeInteraction(select);
    }
    select = selectSingleClick;
    map.addInteraction(select);
}
changeInteraction();

// Custom polygons //

const customPolygonsVectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://127.0.0.1:8000/custompolygons/',
});

const customPolygonsVectorLayer = new ol.layer.Vector({
    source:customPolygonsVectorSource,
    style: new ol.style.Style({
        fill: new ol.style.Fill({ color: 'rgba(255, 2, 2, 0.93)' }),
        stroke: new ol.style.Stroke({ color: '#0096ff', width: 2 }),
    }),
    visible: false,
    
});
map.addLayer(customPolygonsVectorLayer);



