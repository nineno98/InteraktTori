
// STÍLUSOK //

const customPolygonsHiddenColorFill = new ol.style.Fill({
    color: 'rgba(17, 6, 220, 0.0)'

});
const customPolygonsHiddenColorStroke = new ol.style.Stroke({
    color: 'rgba(17, 6, 220, 0.0)',
    width: 2,
});
const customPolygonsShowColorFill = new ol.style.Fill({
    color: 'rgba(17, 6, 220, 0.7)'
});

const customPolygonsShowColorStroke = new ol.style.Stroke({
    color: 'rgba(0, 0, 0, 1)',
    width: 2,
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
};

// VEZÉRLŐK //

let CustomPolygonsState = 0;
let DrawState = 0;

class ShowCustomPolygonsControl extends ol.control.Control {
    /**
     * @param {Object} [opt_options] Control options.
     */
    
    constructor(opt_options) {
    const options = opt_options || {};
    const element = document.createElement('div');
    element.className = 'show-custom-polygons-button ol-unselectable ol-control';
    super({
        element: element,
        target: options.target,
    });
        this.state = 0;
        this.button = document.createElement('button');
        this.button.innerHTML = 'N';
        element.appendChild(this.button);

        this.button.addEventListener('click', this.showOrHiddenPolygons ,false );
    }
    testFunc = () => {
        console.log('testing');
    }
    showOrHiddenPolygons = () => {
        const drawingbutton = document.querySelector('.drawing-button')
        const drawbutton = document.querySelector('.hidden-button-control');
        const drawtype = document.querySelector('.draw-type-control');
        if(CustomPolygonsState  == 1){
            this.button.style.background = 'white';
            //this.state = 0;
            CustomPolygonsState = 0;
            
            customPolygonsVectorLayer.setStyle(new ol.style.Style({
                fill: customPolygonsHiddenColorFill,
                stroke: customPolygonsHiddenColorStroke,
                image: new ol.style.Circle({
                    radius: 6,
                    fill: customPolygonsHiddenColorFill,
                    stroke: customPolygonsHiddenColorStroke,
                }),
            }))
            //map.addInteraction(customPolygonSelect);
            map.removeInteraction(customPolygonSelect);
            map.removeInteraction(modify);
           // map.removeInteraction(draw);
            drawbutton.style.display = 'none';
            drawtype.style.display = 'none';
            DrawState = 0;
            drawingbutton.style.background = 'white';
        }else{
            this.button.style.background = 'lightgrey';
            //this.state = 1;
            CustomPolygonsState = 1;
            
            customPolygonsVectorLayer.setStyle(new ol.style.Style({
                fill: customPolygonsShowColorFill,
                stroke: customPolygonsShowColorStroke,
                image: new ol.style.Circle({
                    radius: 6,
                    fill: customPolygonsShowColorFill,
                    stroke: customPolygonsShowColorStroke,
                }),
            }));
            //map.removeInteraction(customPolygonSelect);
            map.addInteraction(customPolygonSelect);
            map.addInteraction(modify);
            //map.addInteraction(draw);
            drawbutton.style.display = 'block';
        }
    }
};

class DrawPointsAndPolygonsControl extends ol.control.Control{
    constructor(opt_options){
        const options = opt_options || {};
        const element = document.createElement('div');
        element.className = 'hidden-button-control ol-unselectable ol-control';
        element.style.display = 'none';

        super({
            element: element,
            target: options.target,
        });
        this.state = 0;
        this.button = document.createElement('button');
        this.button.innerHTML = 'D';
        this.button.className = 'drawing-button'
        this.button.addEventListener('click', this.enableDraw, false);
        element.appendChild(this.button);

    }

    enableDraw = () => {
        const drawtype = document.querySelector('.draw-type-control');
        if(DrawState == 1){
            DrawState = 0;
            //console.log(CustomPolygonsState+" "+DrawState)
            this.button.style.background = 'white';
            //map.removeInteraction(draw);
            drawtype.style.display = 'none';
        }else{
            DrawState = 1;
            //console.log(CustomPolygonsState+" "+DrawState)
            this.button.style.background = 'lightgrey';
            //map.addInteraction(draw)
            drawtype.style.display = 'block';
        }
    }
}

class DrawTypeControl extends ol.control.Control{
    constructor(opt_options){
        const options = opt_options || {};
        const element = document.createElement('div');
        element.className = 'draw-type-control ol-unselectable ol-control';
        element.style.display = 'none';

        element.innerHTML = `
          <span class="input-group">
              <label class="input-group-text" for="type">Geometry type:</label>
              <select class="form-select" id="geom-type">
                <option value="Point">Point</option>
                <option value="LineString">LineString</option>
                <option value="Polygon">Polygon</option>
                <option value="Circle">Circle</option>
                <option value="None">None</option>
              </select>
              <input class="form-control" type="button" value="Undo" id="undo">
          </span>`;
        super({
            element: element,
            target: options.target,
        });

    };
}

// MAP //

const map = new ol.Map({
    controls: ol.control.defaults.defaults({
        zoom : false,
    }).extend([
        //new ShowCustomPolygonsControl(),
        //new DrawPointsAndPolygonsControl(),
        //new DrawTypeControl(),
    ]),
    
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

//  TERRITORES LAYER //

const vectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://127.0.0.1:8000/territories/' 
});

/*const styleFunction = (feature) => {
    
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
};*/

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
/*function selectStyle(feature) {
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
}*/

const selectSingleClick = new ol.interaction.Select({
    style: selectStyle,
    layers: [vectorLayer]
});

function changeInteraction() {
    if (select !== null) {
        map.removeInteraction(select);
    }
    select = selectSingleClick;
    map.addInteraction(select);
}
changeInteraction();

// CUSTOM POLYGONS//

const customPolygonsVectorSource = new ol.source.Vector({
    format: new ol.format.GeoJSON(),
    url: 'http://127.0.0.1:8000/custompolygons/',
});

const customPolygonsVectorLayer = new ol.layer.Vector({
    source:customPolygonsVectorSource,
    style: new ol.style.Style({ 
        fill: customPolygonsHiddenColorFill,
        stroke: customPolygonsHiddenColorStroke,
        image: new ol.style.Circle({
            radius: 6,
            fill: customPolygonsHiddenColorFill,
            stroke: customPolygonsHiddenColorStroke,
        }),
    }),
    
    
});
map.addLayer(customPolygonsVectorLayer);

const customPolygonSelect = new ol.interaction.Select({
    
    style: new ol.style.Style({ 
        fill: new ol.style.Fill({ color: 'rgba(255, 255, 0, 0.5)' }),  
        stroke: new ol.style.Stroke({ color: '#ff0000', width: 3 })
    }),
    layers: [customPolygonsVectorLayer],
});
//map.addInteraction(customPolygonSelect);
const modify = new ol.interaction.Modify({ source: customPolygonsVectorSource });
//map.addInteraction(modify);




let draw; // global so we can remove it later

function addInteraction() {
    map.removeInteraction(draw);
  const value = "Point"
  if (value !== 'None') {
    draw = new ol.interaction.Draw({
      source: customPolygonsVectorSource,
      type: "Point",
      
      
    });
    map.addInteraction(draw);
    
    

    
  }
  draw.on('drawend', function (event) {
    const feature = event.feature; // Az újonnan rajzolt feature (pont)
    const coordinates = feature.getGeometry().getCoordinates(); // A pont koordinátái
  
    // Log funkció, amely a pont koordinátáit írja ki
    console.log('Pont koordinátái:', coordinates);
  });
}

drawType.addEventListener('change', function () {
    if (draw) {
        map.removeInteraction(draw);
    }
    addInteraction();
});
addInteraction();

























/*
const drawType = document.getElementById('geom-type');
let draw = new ol.interaction.Draw({
    source: customPolygonsVectorSource,
    type: 'Point',
});
drawType.addEventListener('change', function () {
    if (draw) {
        map.removeInteraction(draw);
    }
    addInteraction();
});

function addInteraction() {
    const value = drawType.value;
    if (value !== 'None') {
        draw = new ol.interaction.Draw({
            source: customPolygonsVectorSource,
            type: value,
            
            
            
            
        });
        
        

        map.addInteraction(draw);
    }
}

draw.addEventListener('drawend', (feature) => {
    console.log(feature);
});

/*
console.log(drawType.value);
let draw = new ol.interaction.Draw({
    source: customPolygonsVectorSource,
    type: "Polygon",
});
drawType.onchange = function () {
    map.removeInteraction(draw);
    addNewInteraction();
  };

function addNewInteraction(){
    
    draw = new ol.interaction.Draw({
        source: customPolygonsVectorSource,
        type: "Point",
    });
    map.addInteraction(draw);
    
}
/*const draw = new ol.interaction.Draw({
    source: customPolygonsVectorSource,
    type: "Point",
});*/
//drawType.onchange();*/
