require([
  "esri/config",
  "esri/Map",
  "esri/layers/CSVLayer",
  "esri/views/SceneView",
  "esri/layers/TileLayer",
  "esri/Basemap"
], function (esriConfig,Map, CSVLayer, SceneView, TileLayer, Basemap) {
  // If CSV files are not on the same domain as your website, a CORS enabled server or a proxy is required.
  esriConfig.apiKey = "AAPKdd8f779062f94c55963b952ceccafe35B8vpAe5Gjw3wD6ylKsvWZUpaAuB09RbsCmXgcFmqwuq63wpZkklpwoWQQGLxapO6";
  const url = 
      "/static/data.csv";
  //"https://developers.arcgis.com/javascript/latest/sample-code/layers-csv/live/earthquakes.csv"; 
  const home = window.location.href.replace("globe", "city_activities")

  const template = {
    overwriteActions: true,
    buttonEnabled: false,
    defaultPopupTemplateEnabled: false,
    title: "{place}",
    content: `Plan your trip by checking out things to do in {place}. <br>

      <a class="btn btn-outline-primary" href="${home}/{id}">Click here</a> to find restaurants and activities!`
  };

  const csvLayer = new CSVLayer({
    url: url,
    copyright: "USGS Earthquakes",
    popupTemplate: template
  });


  csvLayer.renderer = {
    type: "simple", // autocasts as new SimpleRenderer()
    symbol: {
      type: "point-3d", // autocasts as new PointSymbol3D()
      // for this symbol we use 2 symbol layers, one for the outer circle
      // and one for the inner circle
      symbolLayers: [
        {
          type: "icon", // autocasts as new IconSymbol3DLayer()
          resource: { primitive: "circle" },
          material: { color: [255, 84, 54, 0.6] },
          size: 5
        },
        {
          type: "icon", // autocasts as new IconSymbol3DLayer()
          resource: { primitive: "circle" },
          material: { color: [255, 84, 54, 0] },
          outline: { color: [255, 84, 54, 0.6], size: 1 },
          size: 10
        }
      ]
    }
  };


  const map = new Map({
    basemap: new Basemap({
      baseLayers: [
        new TileLayer({
          url: "https://tiles.arcgis.com/tiles/nGt4QxSblgDfeJn9/arcgis/rest/services/terrain_with_heavy_bathymetry/MapServer"
        })
      ]
    }),
    layers: [csvLayer]
  });

  const view = new SceneView({
    container: "viewDiv",
    map: map,
    // Indicates to create a global scene
    viewingMode: "global",
    camera: {
      position: [
        -63.77153412,
        20.75790715,
        25512548.00000
      ],
      heading: 0.00,
      tilt: 0.10
    },
    constraints: {
      altitude: {
        min: 700000
      }
    },
    qualityProfile: "high",
    alphaCompositingEnabled: true,
    highlightOptions: {
      fillOpacity: 0,
      color: "#ffff"
    },
    environment: {
      background: {
        type: "color",
        color: [51,41,74, 30]
      },
      atmosphere: null,
      starsEnabled: true
    }
  });

});