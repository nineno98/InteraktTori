const hatter = new ol.layer.Tile({
    source: new ol.source.OSM(),
  });
  
const drawingSource = new ol.source.Vector({wrapX: false});
  
const drawingLayer = new ol.layer.Vector({
    source: drawingSource,
  });


class TerritoriesVectorLayer{
    constructor(apiUrl){
        this.apiUrl = apiUrl;
        this.vectorSource = new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            url: this.apiUrl,
        });
        this.vectorLayer = new ol.layer.Vector({
            source: this.vectorSource,
            style: this.SetStyleFunction.bind(this),
        });

        this.vectorSource.once('addfeature', (event) => {    
            this.filterByDate({ target: { value: -700 } });
        });

        this.dateSlider = document.getElementById('date-slider');
        this.dateSlider.addEventListener('input', this.filterByDate.bind(this), false);
    }

    SetStyleFunction(feature){
        //let color = ol.color.asArray(feature.get('color')).slice();
        //let color = feature.get('color');
        //console.log(color);
        //color[3] = 0.7;
        

        var hexColor = feature.get('color');
        var color = ol.color.asArray(hexColor);
        color = color.slice();
        color[3] = 0.7;
        console.log(color);
        let strokeColor = this.rgbaColorDarker(color.slice(), 0.1);
        //console.log(strokeColor);

        if(feature.get('hidden')){
            return null;
        }
        return new ol.style.Style({
            fill: new ol.style.Fill({
              color: color,
            }),
            stroke: new ol.style.Stroke({
              color: strokeColor,
              width: 2,
            }),
        });
    }

    filterByDate(event){
        let selectedDate = parseInt(event.target.value);
        document.getElementById('slider-value').textContent = selectedDate;
        console.log('filtering')
        this.vectorSource.forEachFeature((feature) => {
            let stard_date = feature.get('start_date')
            let end_date = feature.get('end_date')
            if(selectedDate < stard_date || selectedDate >= end_date){
                feature.set('hidden', true);
            }else{
                feature.set('hidden', false);
            }
    
            feature.changed()
        });
    }

    getLayer(){
        return this.vectorLayer;
    }

    rgbaColorDarker(colorArray, darkerFaktor){
        try{
            if(colorArray.length == 4){
                colorArray[0] = Math.round(Math.max(0, colorArray[0] * darkerFaktor)); // R
                colorArray[1] = Math.round(Math.max(0, colorArray[1] * darkerFaktor)); // G
                colorArray[2] = Math.round(Math.max(0, colorArray[2] * darkerFaktor)); // B

                colorArray[3] = Math.max(0, Math.min(1, colorArray[3])); // Átlátszóság

                return colorArray;
            }else{
                throw new Error("Nem megfelelő a megadott tömb alakja. csak rgba-t tároló megfelelő.");
            }
        }
        catch (error) {
            console.error('Hiba történt a szín sötétítésekor: ', error.message);
        }
        
    }

}

const territories = new TerritoriesVectorLayer('http://127.0.0.1:8000/territories/');


  const map = new ol.Map({
    layers: [
        hatter,
        territories.getLayer(),
        drawingLayer,
        

    ],
    target: 'map',
    view: new ol.View({
      center: ol.proj.fromLonLat([12.496366, 41.902782]),
      zoom: 4,
      projection: 'EPSG:3857',
    }),
  });
  
  class HandleDraw {
    constructor(){
        this.undoButton = document.getElementById('undo');
        this.undoButton.addEventListener('click', this.undoHandling.bind(this), false);
        this.typeSelect = document.getElementById('type');
        this.typeSelect.addEventListener('change', this.changeHandle.bind(this), false);
        this.draw = null;
    }
    addInteraction() {
        const value = this.typeSelect.value;
        if (value !== 'None') {
          this.draw = new ol.interaction.Draw({
            source: drawingSource,
            type: this.typeSelect.value,
          });
          map.addInteraction(this.draw);
        }
    }
    changeHandle(){
        map.removeInteraction(this.draw);
        this.addInteraction();
    }

    undoHandling(){
        this.draw.removeLastPoint();
    }

    turnOffDaw(){
        map.removeInteraction(this.draw);
    }
  }

  const handledraw = new HandleDraw();
  handledraw.addInteraction();

  /*const typeSelect = document.getElementById('type');
  
  let draw; // global so we can remove it later
  function addInteraction() {
    const value = typeSelect.value;
    if (value !== 'None') {
      draw = new ol.interaction.Draw({
        source: source,
        type: typeSelect.value,
      });
      map.addInteraction(draw);
    }
  }
  
  
  /**
   * Handle change event.
   
  typeSelect.onchange = function () {
    map.removeInteraction(draw);
    addInteraction();
  };
  
  document.getElementById('undo').addEventListener('click', function () {
    draw.removeLastPoint();
  });
  
  addInteraction();*/