const hatter = new ol.layer.Tile({
    source: new ol.source.OSM(),
  });
  
//const drawingSource = new ol.source.Vector({wrapX: false});
  
/*const drawingLayer = new ol.layer.Vector({
    source: drawingSource,
  });*/


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
        
        var hexColor = feature.get('color');
        var color = ol.color.asArray(hexColor);
        color = color.slice();
        color[3] = 0.7;
        let strokeColor = this.rgbaColorDarker(color.slice(), 0.2);
        let featureName = this.capitalizeFirstCharacters(feature.get('name')) || 'N/A';
        let start_date = this.handleDates(feature.get('start_date') || 'N/A');
        let end_date = this.handleDates(feature.get('end_date') || 'N/A');
        

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
            text: new ol.style.Text({
                font: '14px Arial',
                fill: new ol.style.Fill({ color: '#000' }),
                stroke: new ol.style.Stroke({ color: '#fff', width: 2 }),
                text: `${featureName}\n${start_date} - ${end_date}`,
                offsetY: -10,
            }),
        });
    }

    filterByDate(event){
        let selectedDate = parseInt(event.target.value);
        document.getElementById('slider-value').textContent = selectedDate;
        //console.log('filtering')
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
            console.error('rgbaColorDarker: Hiba történt a szín sötétítésekor: ', error.message);
        } 
    }
    capitalizeFirstCharacters(value){
        try{
            if(typeof value == 'string')
                return String(value).charAt(0).toUpperCase() + String(value).slice(1);
            else
                throw new Error("A value érték nem string")
        }catch (error) {
            console.error('capitalizeFirstCharacters: Hiba:'+error.message);
        }
    }
    handleDates(value){
        try{
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
        }catch (error) {
            console.error('handleDates: Hiba:'+error.message);
        }
        
    }

}


  
  class HandleDraw {
    constructor(apiUrl){
        this.apiUrl = apiUrl;
        this.drawenabled = false;
        this.selectenabled = false;
        this.select = null;
        this.draw = null;
        this.modify = null;

        this.selectedStyle = new ol.style.Style({
            fill: new ol.style.Fill({
                color: 'rgba(233,84,33,0.5)', 
            }),
            stroke: new ol.style.Stroke({
                color: 'blue',
                width: 2,
            }),
        })

        this.drawingSource = new ol.source.Vector({
            wrapX: false,
            format: new ol.format.GeoJSON(),
            url: this.apiUrl,

        });
  
        this.drawingLayer = new ol.layer.Vector({
            source: this.drawingSource,
        });

        this.undoButton = document.getElementById('undo');
        this.undoButton.addEventListener('click', this.undoHandling.bind(this), false);

        this.typeSelect = document.getElementById('type');
        this.typeSelect.addEventListener('change', this.changeHandle.bind(this), false);

        this.drawenableButton = document.getElementById('draw-enable');
        this.drawenableButton.addEventListener('click', this.enableDraw.bind(this), false);

        this.selectenableButton = document.getElementById('select-enable');
        this.selectenableButton.addEventListener('click', this.enableSelect.bind(this), false);

        

        
    }


    addSelect(){
        this.select = new ol.interaction.Select({
            layers: [this.drawingLayer],
            style: this.selectedStyle,
        });
        map.addInteraction(this.select);
        this.modify = new ol.interaction.Modify({
            features: this.select.getFeatures()
        });
        map.addInteraction(this.modify);
    }

    addInteraction() {
        const value = this.typeSelect.value;
        if (value !== 'None') {
          this.draw = new ol.interaction.Draw({
            source: this.drawingSource,
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

    getLayer(){
        return this.drawingLayer;
    }

    turnOnDraw(){
        this.addInteraction();
    }

    enableDraw(){
        if(!this.drawenabled){
            if(this.selectenabled){
                map.removeInteraction(this.select);
                map.removeInteraction(this.modify);
                this.selectenabled = false;
            }
            this.drawenabled = true;
            this.turnOnDraw();
            
        }
        else{
            this.drawenabled = false;
            this.turnOffDaw();
        }
    }

    enableSelect(){
        if(!this.selectenabled){
            if(this.drawenabled){
                this.drawenabled = false;
                this.turnOffDaw();
            }
            this.selectenabled = true;
            this.addSelect();
            
        }
        else{
            this.selectenabled = false;
            map.removeInteraction(this.select);
            map.removeInteraction(this.modify);
        }
    }
  }



  const territories = new TerritoriesVectorLayer('http://127.0.0.1:8000/territories/');
const drawing = new HandleDraw('http://127.0.0.1:8000/custompolygons/')

  const map = new ol.Map({
    layers: [
        hatter,
        territories.getLayer(),
        drawing.getLayer(),
        

    ],
    target: 'map',
    view: new ol.View({
      center: ol.proj.fromLonLat([12.496366, 41.902782]),
      zoom: 4,
      projection: 'EPSG:3857',
    }),
  });


  /*const handledraw = new HandleDraw();
  handledraw.addInteraction();*/

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