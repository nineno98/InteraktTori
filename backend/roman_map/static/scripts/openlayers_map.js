const hatter = new ol.layer.Tile({
    source: new ol.source.OSM(),
  });
  
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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
            image: new ol.style.Circle({
                radius: 8,
                fill: new ol.style.Fill({ color: 'yellow' }),
                stroke: new ol.style.Stroke({ color: 'red', width: 2 })
            }),
            text: new ol.style.Text({
                font: 'bold 14px Arial',
                fill: new ol.style.Fill({ color: 'black' }),
                stroke: new ol.style.Stroke({ color: 'white', width: 2 }),
                offsetY: -15, // A szöveg eltolása felfelé
                text: function(feature) { return feature.get('name') || ''; }
            })
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

    selectedStyleFunction(feature){
        const zoom = map.getView().getZoom();
        return [
            new ol.style.Style({
                fill: new ol.style.Fill({
                    color: 'rgba(233,84,33,0.5)', 
                }),
                stroke: new ol.style.Stroke({
                    color: 'blue',
                    width: 2,
                }),
                image: new ol.style.Circle({
                    radius: 8,
                    fill: new ol.style.Fill({ color: 'yellow' }),
                    stroke: new ol.style.Stroke({ color: 'red', width: 2 })
                }),
                text: new ol.style.Text({
                    font: 'bold 14px Arial',
                    fill: new ol.style.Fill({ color: 'black' }),
                    stroke: new ol.style.Stroke({ color: 'white', width: 2 }),
                    offsetY: -15, // A szöveg eltolása felfelé
                    text: zoom > 5 ? feature.get('name') || '' : '', 
                })
            })
        ]
    }

    addSelect(){
        this.select = new ol.interaction.Select({
            layers: [this.drawingLayer],
            style: this.selectedStyleFunction,
        });
        map.addInteraction(this.select);
        this.modify = new ol.interaction.Modify({
            features: this.select.getFeatures()
        });
        map.addInteraction(this.modify);
        
        let originalGeometry = null;
        const selectedFeatures = this.select.getFeatures();

        this.modify.on('modifystart', function (event) {
            console.log('módosítás elkezdődött');
            if (selectedFeatures.getLength() > 0) {
                const feature = selectedFeatures.item(0);
                originalGeometry = feature.getGeometry().clone();
            }
        });
        this.modify.on('modifyend', (event) => {
            console.log('modositas vege');
            if (selectedFeatures.getLength() > 0) {
                const feature = selectedFeatures.item(0);
                this.modifyPopup(feature, originalGeometry);
            }
        });

        const deletingBundle = () =>{
            if(selectedFeatures.getLength() > 0){
                const feature = selectedFeatures.item(0);
                this.deletePopup(feature);
            }
            else{
                alert('A törléshez előbb ki kell jelölnöd egy elemet!')
            }
        }

        const deleteButton = document.getElementById('delete-selected-feature');
        deleteButton.removeEventListener('click', deletingBundle);
        deleteButton.addEventListener('click',  deletingBundle);
        
    }

    deletePopup(feature){
        const popupContainer = document.getElementById('delete-popup');
        const saveButton = document.getElementById('deleteFeatureButton');
        const closeButton = document.getElementById('closeDeletingPopup');

        popupContainer.style.display = 'block';
        closeButton.removeEventListener('click', this.closeDeleting);
        saveButton.removeEventListener('click', this.acceptDeleting);

        this.closeDeleting = () => {
            popupContainer.style.display = 'none';
        }
        closeButton.addEventListener('click', this.closeDeleting);

        this.acceptDeleting = () => {
            const featureId = feature.get('id');
            const csrftoken = getCookie('csrftoken')
            console.log('document.cookie:', document.cookie);
            console.log(csrftoken)
            fetch('http://127.0.0.1:8000/custom-draws/',{
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id:featureId
                })
            }).then(response => {
                if(response.ok){
                    console.log('Feature törölve az adatbázisból');
                    this.drawingLayer.getSource().removeFeature(feature);
                    popupContainer.style.display = 'none';
                    console.log("Feature törölve:", feature);

                    map.removeInteraction(this.select);
                    map.removeInteraction(this.modify);
                    this.addSelect();
                }else{
                    console.error('Hiba a törlés során:', response.statusText);
                }
            }).catch(error => {
                console.error('Hálózati hiba történt:', error);
            });

            /*console.log('accept deleting feature id: '+featureId);
            this.drawingLayer.getSource().removeFeature(feature);
            popupContainer.style.display = 'none';
            console.log("Feature törölve:", feature);

            map.removeInteraction(this.select);
            map.removeInteraction(this.modify);
            this.addSelect();*/
        }
        saveButton.addEventListener('click', this.acceptDeleting);

    }

    modifyPopup(feature, originalGeometry){
        const popupContainer = document.getElementById('modify-popup');
        const saveButton = document.getElementById('modifiFeature');
        const closeButton = document.getElementById('closeModifyPopup');

        popupContainer.style.display = 'block';
        closeButton.removeEventListener('click', this.closeModify);
        saveButton.removeEventListener('click', this.saveModify);

        this.closeModify = () =>{
            popupContainer.style.display = 'none';
            feature.setGeometry(originalGeometry);
            map.removeInteraction(this.select);
            map.removeInteraction(this.modify);

            
            this.addSelect();
        };
        closeButton.addEventListener('click', this.closeModify);

        this.saveModify = () => {
            console.log('mentes');
            const featureId = feature.get('id');
            const csrftoken = getCookie('csrftoken')
            const cloneFeature = feature.clone();
            cloneFeature.getGeometry().transform('EPSG:3857', 'EPSG:4326');
            const coordinates4326 = cloneFeature.getGeometry().getCoordinates();
            console.log(coordinates4326);
            fetch('http://127.0.0.1:8000/custom-draws/', {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    id : featureId,
                    coordinates : coordinates4326
                })
            }).then(response => {
                if(response.ok){
                    console.log('Feature módosítva az adatbázisban');
                    popupContainer.style.display = 'none';
                    
                    //this.selectenabled = false;
                    map.removeInteraction(this.select);
                    map.removeInteraction(this.modify);
                    //this.drawingLayer.getSource().changed();

                    //this.selectenabled = true;
                    this.addSelect();

                }else{
                    popupContainer.style.display = 'none';
                    feature.setGeometry(originalGeometry);
                    console.error('Hiba a törlés során:', response.statusText);
                    map.removeInteraction(this.select);
                    map.removeInteraction(this.modify);
                    this.drawingLayer.getSource().changed();

                    //this.selectenabled = true;
                    this.addSelect();
                }
            }).catch(error => {
                console.error('Hálózati hiba történt:', error);
            });
            //this.drawingLayer.getSource().changed();
            
            

            
        };
        saveButton.addEventListener('click', this.saveModify);

        

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
        this.draw.on('drawend', (event) => {
            this.saveDrawPopUp(event.feature);
        });

    }

    saveDrawPopUp(feature){
        const popupContainer = document.getElementById('draw-popup');
        
        const saveButton = document.getElementById('saveFeature');
        const closeButton = document.getElementById('closePopup');
        
        //const description = descriptionInput.value.trim();
        const errorLabel = document.getElementById('nameError');

        popupContainer.style.display = 'block';

        closeButton.removeEventListener('click', this.closePopupHandler);
        saveButton.removeEventListener('click', this.saveFeatureHandler);

        this.closePopupHandler = () => {
            popupContainer.style.display = 'none';
            this.drawingSource.removeFeature(feature);
            alert("A rajz megőrzéséhez előbb mentened kell azt!");
        };
        closeButton.addEventListener('click', this.closePopupHandler);

        this.saveFeatureHandler = () => {
            console.log(feature.getGeometry().getCoordinates());
            //popupContainer.style.display = 'none';
            const name = document.getElementById('name').value;
            const description = document.getElementById('description').value;
            const created_by = document.querySelector('meta[name="user-id"]').content
            console.log(created_by);
            if(!name){
                errorLabel.textContent = "A név megadása kötelező!";
                errorLabel.style.display = "block";
                return;
            }
            else{
                popupContainer.style.display = 'none';
                document.getElementById('name').value = '';
                document.getElementById('description').value = '';
                feature.setProperties({ name, description, created_by });
                const csrftoken = getCookie('csrftoken')
                const format = new ol.format.GeoJSON({
                    dataProjection: 'EPSG:4326',
                    featureProjection: 'EPSG:3857'
                });
                const geojson = format.writeFeatureObject(feature);
                
                fetch('http://127.0.0.1:8000/custom-draws/', {
                    method:'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(geojson)


                }).then(response => {
                    if(response.ok){
                        console.log("Mentés sikeresen megtörtént");
                        return response.json()
                        /*const data = response.json();
                        const id = data.id;
                        feature.setProperties({id})

                        this.turnOffDaw();
                        
                        this.turnOnDraw();*/
                    }else{
                        console.log("Mentés sikertelen.");
                        this.drawingLayer.getSource().removeFeature(feature)
                        return Promise.reject("Sikertelen mentés");
                    }
                }).then(data => {
                    const id = data.id;
                    feature.setProperties({id})

                    this.turnOffDaw();
                    this.turnOnDraw();
                }).catch(error => {
                    console.error("Hiba:", error);
                });            
            }
            
        };
        saveButton.addEventListener('click', this.saveFeatureHandler);

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
const drawing = new HandleDraw('http://127.0.0.1:8000/custom-draws/')

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