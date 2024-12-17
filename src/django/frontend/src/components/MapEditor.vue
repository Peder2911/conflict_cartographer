<template>
   <div id="mapeditor">
      <div id="map" ref="map"></div>

      <!-- Overlays -->

      <!-- Controls -->
      <vue100vh class="overlay" id="map-editor-overlay">
         <div id="map-editor-overlay-header">
         </div>

         <div id="map-editor-overlay-viewport">
         </div>

         <div id="map-editor-overlay-controlbar">

            <!-- Buttons -->
            <div id="map-editor-overlay-buttons">
               <div v-if="mode===1" id="mode-select">
                  <button title="Draw a prediction shape"
                     id="draw-button" v-on:click="startdraw">Draw</button>
                  <button title="Erase prediction shapes"
                     id="erase-button" v-on:click="startdelete">Erase</button>
               </div>

               <div v-else id="mode-cancel">
                  <button title="Show actions"
                     id="neutral-button" v-on:click="neutral">Ok</button>
               </div>

               <div> 
                  <button title="Submit predictions"
                     id="submit-button" v-on:click="$router.push('/')">Submit</button>
                  <button title="Submit 'No conflict'"
                     v-if="allow_rescind" id="nonanswer-button" v-on:click="non_answer">No conflict</button>
               </div> 
            </div>

            <!-- Layer editor -->
            <div v-if="selectedLayer !== undefined" id="layer-editor-popup">
               <div id="scale-inputs" class="upper">
                  <div class="scale-input">
                     <h2>Intensity</h2>
                     <div class="intensity-input" v-for="choice in choices" :key="choice.key">
                        <input type="radio" v-model="selectedLayer.feature.properties.intensity" :value="choice.value">
                        <label class="cat-label" :for="choice.key">{{ choice.key }}</label>
                     </div>
                  </div>
                  <div class="scale-input">
                     <h2>Confidence</h2>
                     <vue-slider 
                        v-model="selectedLayer.feature.properties.confidence"
                        :min="0"
                        :max="100"
                        :interval="1"
                        >
                     </vue-slider>
                  </div>
               </div>
               <button title="Submit prediction shape values"
                  v-on:click="deselect" class="continue">Ok</button>
            </div>
         </div>
      </vue100vh>

      <!-- When am i predicting for -->
      <div v-if="pred_start!==undefined" class="overlay" id="prediction-period-display">
         <div>
            <h1>Predicting for<br>{{ pred_start }} - {{ pred_end }}</h1>
         </div>
      </div>

      <!-- Right slideover -->
      <Slideover 
         v-on:was-closed="set_was_informed"
         :start_open="start_open" :size="300" :direction="2">
         <div id="right-info">
            <h2>Variable definition</h2>
               <p>
                  For this survey, we use the UCDP GED definition of conflict.
                  Under this definition, conflict is defined as:
               </p>
               <p class="definition">
                  [A]n incident where armed force was used by an organized actor
                  against another organized actor, or against civilians,
                  resulting in at least one (1) direct death at a specific
                  location and a specific date.
               </p>
               <p class="attribution">
                  Sundberg, Ralph and Erik Melander (2013) Introducing the
                  UCDP Georeferenced Event Dataset. Journal of Peace Research
                  50(4)
               </p>
               <p>
                  We ask for a prediction of conflict intensity. In addition,
                  you are asked to provide your measure of confidence in the
                  prediction. Confidence is measured on a simple scale of
                  1-100% which corresponds to your estimate of the chance of
                  your prediction being correct, against the chance of it not
                  being correct (meaning there was less or more intensity in
                  the indicated area than you predicted).
               </p>
               <p>
                  To begin adding predictions, navigate to an area of interest,
                  press "draw", and draw an area on the map. You are then asked
                  to add values for conflict intensity and confidence.
               </p>
               <p>
                  Click the arrow to close this dialogue box.
               </p>
         </div>
      </Slideover>

      <!-- Big helptext -->
      <HelptextOverlay>
         <h1>
            {{ this.helptexts[this.mode].title }}
         </h1>
         {{ this.helptexts[this.mode].text }}
      </HelptextOverlay>

      <transition name="fade">
         <div v-if="!loaded" id="loading-cover" class="overlay">
            <Spinner v-if="!loaded"></Spinner>
         </div>
      </transition>

   </div>
</template>
<style scoped lang="sass">
@import "../sass/variables.sass"

.definition
   font-style: italic
   padding: 10px 0
   border: 1px solid #ccc
   border-left: none
   border-right: none

.attribution
   font-size: 12px


.fade-enter-active, .fade-leave-active
   transition: opacity 1s
.fade-enter, .fade-leave-to
   opacity: 0

#loading-cover
   background: $ui-gray
   pointer-events: auto
   z-index: 9999
   display: grid
   place-items: center

#right-info
   width: 100%
   height: 100%
   background: #f0f0f0
   color: #222
   padding: 10px
   padding-left: 20px
   border-left: 4px solid #aaa

#prediction-period-display
   text-align: center
   font-size: 8px
   color: white 
   margin: 0
   padding: 0 60px
   max-width: 320px 

#prediction-period-display h1
   background: $ui-highlight
   border-radius: 10px

@media only screen and (min-width: $mob-width)
   #prediction-period-display
      margin: auto 
      font-size: 16px
      max-width: $mob-width

#map-editor-overlay
   display: grid
   grid-template-rows: 25px auto 80px
   justify-items: center
   overflow: hidden
   height: 100vh
   width: 100vw

#map-editor-overlay-header
   display: grid
   grid-auto-flow: column
   grid-template-column: repeat(auto-fill, 1fr)
   width: 100%

#map-editor-overlay-header>div
   border: 1px solid redgray 
   background: $ui-highlight

#map-editor-overlay-controlbar
   //display: grid
   //place-items: center
   pointer-events: auto
   position: relative

#map-editor-overlay-buttons
   width: 100vw 
   height: 100%
   display: grid
   grid-auto-flow: column
   grid-template-columns: 1fr 1fr 
   grid-gap: 10px
   padding: 10px
   background: $ui-darkergray

#draw-button
   background: $ui-gray
   color: #222

#erase-button
   background: $ui-highlight
   
#neutral-button
   background: $ui-gray
   color: #222

#submit-button
   background: $ui-gray
   color: #222

#nonanswer-button
   background: $ui-progress-alt 

#map-editor-overlay-buttons button
   height: 100% 
   border-bottom: 4px solid #222

#map-editor-overlay-buttons div 
   display: grid
   grid-auto-flow: column
   grid-gap: 10px

$popup-height: 280px

@keyframes pop-up
   0%
      transform: translateY($popup-height)
   100%
      transform: translateY(0)

#layer-editor-popup
   position: absolute
   bottom: 0
   left: 0

   border-radius: 10px 10px 0 0
   padding: 10px 20px

   display: grid
   grid-template-rows: 3fr 1fr 
   grid-gap: 10px

   height: $popup-height
   width: 100%

   background: $ui-darkergray

   animation-name: pop-up
   animation-duration: 0.2s 
   animation-fill-mode: forwards

   z-index: 99


#layer-editor-popup label
   font-size: 20px 

#layer-editor-popup button
   background: $ui-gray
   border-bottom: 4px solid #222 
   color: #222

#scale-inputs
   display: grid

.scale-input
   background: rgba(255,255,255,0.1)
   padding: 10px 20px
   color: white
   border-bottom: 1px solid #222

.scale-input>h2
   color: white
   margin: 0

@media only screen and (min-width: $mob-width)
   #map-editor-overlay-buttons
      width: $mob-width
      border-radius: 10px 10px 0 0

   #map-editor-overlay-controlbar
      width: $mob-width

$darken: 0.4

#map
   height: 100vh
   width: 100vw
   background: #aaa 
   filter: contrast(1) // Somehow necessary for proper Z indexing

#mapeditor
  -webkit-font-smoothing: antialiased
  -moz-osx-font-smoothing: grayscale
  color: #2c3e50

// Editing dots
.leaflet-editing-icon
   //width: 5px !important
   //height: 5px !important
   //top: 5px !important 
   //left: 5px !important
   border-radius: 10px
   border: none
   background: $drawcolor

.leaflet-marker-pane div:nth-child(2)
   background: $ui_highlight


.leaflet-touch .leaflet-control-zoom-display 
  width: $tbsize + 8px
  height: $tbsize + 8px
  font-size: 18px
  line-height: $tbsize - ($tbsize / 4) 
.leaflet-touch .leaflet-bar a, .leaflet-touch .leaflet-toolbar-0 > li > a 
  width: $tbsize + 4px
  height: $tbsize + 4px
  font-size: $tbsize / 2 
  line-height: $tbsize + 5px
  background-size: 314px 30px
.leaflet-touch .leaflet-draw-toolbar.leaflet-bar a 
  background-position-y: 6px
.leaflet-touch .leaflet-draw-actions a, .leaflet-touch .leaflet-control-toolbar .leaflet-toolbar-1 > li > .leaflet-toolbar-icon 
  font-size: $tbsize / 2 
  line-height: $tbsize + 4px
  height: $tbsize + 4px
.leaflet-touch .leaflet-draw-actions, .leaflet-touch .leaflet-toolbar-1 
  left: $tbsize + 5px
.leaflet-touch .leaflet-control-layers, .leaflet-touch .leaflet-bar
   border: none

</style>

<script>
//import {LMap, LGeoJson} from "vue2-leaflet"
import L from "leaflet"

import "leaflet-draw" 
import "leaflet-boundary-canvas"
import bbox from "geojson-bbox"

import "@/sass/leaflet_custom.sass"

import colorGradient from "@/util/colorGradient.js"
import HelptextOverlay from "@/components/HelptextOverlay"
import Slideover from "@/components/Slideover"
import Spinner from "@/components/widgets/Spinner"

import VueSlider from "vue-slider-component"
import "vue-slider-component/theme/default.css"
import "@/sass/vueslider.sass"

import vue100vh from "vue-100vh"

import {configure_map,shape_to_latlng_box,fit_to_geojson} from "@/configure_map"

import debounce from "@/util/debounce"

import {format_date} from "@/date_formatting"

L.drawLocal.draw.handlers.polygon.tooltip.start = ""

const COLORS={
   low: "#2b83ba",
   high: "#d7191c",
}

const MODES={
   neutral: 1,
   drawing: 2,
   deleting: 3,
   editing: 4
}

const HELPTEXTS={
   1: {
      title:"Data entry",
      text:"Click draw to begin",
   },
   2: {
      title:"Draw",
      text:"Draw a shape by clicking to place vertices.",
   },
   3: {
      title:"Erase",
      text:"Click shapes to erase them",
   },
   4: {
      title:"Editing",
      text:"Change the values of a shape",
   }
}

const BASE_STYLE = {
   fillOpacity: 0.3,
   opacity: 0.2,
   weight: 3
}

export default {
   name: 'MapEditor',
   components: {
      HelptextOverlay,
      VueSlider,
      vue100vh,
      Slideover,
      Spinner,
   },
   
   props: {
      defaultIntensity: {
         default: 0
      },
      defaultConfidence: {
         default: 50 
      },
   },

   data(){
      return {
         loaded: false, 
         infocus: "",

         projectShape: undefined,
         absUrl: undefined,

         map: undefined,

         drawnItems: new L.geoJSON(undefined),
         pendingItems: new L.featureGroup(),

         mode: MODES.neutral,

         selectedLayer: undefined,

         helptexts: HELPTEXTS,

         drawing: undefined,

         choices: [
            {key:"Low (1-25 casualties)",value:0},
            {key:"Medium (26-99 casualites)",value:1},
            {key:"High (>100 casualties)",value:2},
         ],

         pred_start: undefined,
         pred_end: undefined,
         allow_rescind: true,

         start_open: false,
      }
   },

   computed:{
      project_url(){
         return `countries/${this.$route.params.gwno}`
      },
      gwno(){
         return this.$route.params.gwno
      },
      selectedProps(){
         if(this.selectedLayer !== undefined){
            return this.selectedLayer.feature.properties
         } else {
            return undefined
         }
      },
      nchoices(){
         return Object.keys(this.choices).length
      }
   },

   watch: {
      selectedProps: {
         handler(){
            if(this.selectedLayer !== undefined){
               this.updated(this.selectedLayer)
            }
         },
         deep: true
      }
   },
   created(){
      this.start_open = (this.$cookies.get("var_informed")===null)
   },
   mounted: function(){

      this.check_open(()=>{
         this.init_map(()=>{
            this.add_drawn_shapes(()=>{
               this.loaded = true
            })
         })
      })

      this.get_pred_period()

      document.addEventListener("keydown",(e)=>{
         if(e.key=="Escape"){
            this.neutral()
         }
      })
   },

   methods: {
      /* INITIALIZATION */
      check_open(callback){
         this.$api.get.rel("period/open")
            .then((r)=>{
               if(!r.data.open){
                  this.$router.push("/closed")
               } else {
                  if(callback!==undefined){
                     callback()
                  }
               }
            })
      },

      set_was_informed(){
         this.$cookies.set("var_informed",true)
      },

      init_map(callback){
         this.$api.get.rel(this.project_url)
            .then((r)=>{
               this.projectShape = r.data.shape
               this.absUrl = r.data.url

               this.map = new L.Map(this.$refs.map)
               configure_map(this.map,this.projectShape)
               this.map.on(L.Draw.Event.CREATED,(e)=>{
                  this.created(e.layer)
               })

               const box = bbox(this.projectShape)
               const getbox = (box) => [[box[3],box[0]],[box[1],box[2]]]
               const bbox_latlng = L.latLngBounds(getbox(box))

               this.map.fitBounds(bbox_latlng)
               this.map.setMaxBounds(bbox_latlng.pad(2))

               this.pendingItems.addTo(this.map)

               if(callback!==undefined){
                  callback()
               }
            })
      },

      add_drawn_shapes(callback){
         this.$api.get.rel("shapes",{params: {country: this.gwno}})
            .then((r)=>{
               if(r.data.length>0){
                  this.allow_rescind=false
               }

               let features = r.data.map((db_shape)=>{
                  let feature = db_shape.shape
                  feature.properties = db_shape.values 
                  feature.properties.url = db_shape.url
                  return feature 
               })

               this.drawnItems.addData(features)
               this.drawnItems.addTo(this.map)

               this.drawnItems.on("click",(e)=>{this.clicked(e.layer)})
               this.restyle()
               if(callback!==undefined){
                  callback()
               }
            })
            .catch((e)=>{
               console.error(`Error adding layers: ${e}`)
            })
      },

      get_pred_period(){
         this.$api.get.rel("period/next")
            .then((r)=>{
               this.pred_start = format_date(r.data.start)
               this.pred_end = format_date(r.data.end)
            })
            .catch((e)=>{
               console.error(`Error fetching dates: ${e}`)
            })
      },

      /* INTERACTION */
      neutral(){
         this.mode = MODES.neutral
         if(this.drawing !== undefined){
            this.drawing.disable()
         }
         if(this.selectedLayer !== undefined){
            this.selectedLayer.feature.properties.selected = undefined 
         }
         this.restyle()
      },

      startdraw(){
         this.mode = MODES.drawing
         if(this.map !== undefined){
            this.drawing = new L.Draw.Polygon(this.map,{shapeOptions:{color:"grey"}})
            this.drawing.enable()
         }
      },

      startdelete(){
         this.mode = MODES.deleting 
      },

      clicked(layer){
         if(this.mode == MODES.deleting){
            this.deleted(layer)
         } else {
            this.selected(layer)
         }
      },

      deleted(layer){
         if(this.mode == MODES.deleting){
            this.drawnItems.removeLayer(layer)
            if(this.drawnItems.getLayers().length == 0){
               this.allow_rescind = true
            }

            this.$api.del.abs(layer.feature.properties.url)
               .then(()=>{
                  this.drawnItems.removeLayer(layer)
               })
               .catch((e)=>{
                  console.error(e)
                  this.drawnItems.addLayer(layer)
               })
         }
      },

      created(layer){
         this.pendingItems.clearLayers()
         this.pendingItems.addLayer(layer.setStyle({color:"gray",opacity:0.5}))
         this.map.addLayer(this.pendingItems)

         let geojson = layer.toGeoJSON()
         let values = {
            intensity: this.defaultIntensity,
            confidence: this.defaultConfidence,
         }

         let toPost = {
            shape: geojson, 
            values: values,
            country: this.absUrl 
         }

         this.$api.post.rel("shapes",{data:toPost})
            .then((r)=>{
               geojson.properties = values
               geojson.properties.url = r.data.url

               this.drawnItems.addData(geojson)
               this.allow_rescind = false 

               let newlyCreated = this.drawnItems.getLayers().find((lyr)=>lyr.feature.properties.url==r.data.url)
               this.map.removeLayer(this.pendingItems)
               this.selected(newlyCreated)
               this.restyle(newlyCreated)
            })
            .catch((e)=>{
               console.error(e)
            })
      },

      selected(layer){
         if(this.selectedLayer !== undefined){
            this.selectedLayer.feature.properties.selected = undefined
         }

         layer.feature.properties.selected = true
         this.selectedLayer = layer
         this.mode = MODES.editing

         let bbox = shape_to_latlng_box(this.selectedLayer.toGeoJSON()).pad(.5)
         this.map.fitBounds(bbox,{})
         this.restyle()
      },

      deselect(){
         if(this.selectedLayer !== undefined){
            this.selectedLayer.feature.properties.selected = undefined
         }
         this.restyle()
         this.selectedLayer = undefined
         fit_to_geojson(this.map,this.projectShape)
         this.mode = MODES.neutral
      },

      updated(layer){
         // API call
         this.restyle()

         let values ={
            intensity: layer.feature.properties.intensity,
            confidence: layer.feature.properties.confidence,
         }

         let to_post = {
            shape: layer.feature,
            values: values,
            country: this.absUrl,
         }

         this.post_update(layer.feature.properties.url,to_post)
      },

      post_update: debounce(function(url,data){
         this.$api.put.abs(url,{data:data})
            .catch((e)=>{
               console.error(e)
            })
      }, 500),

      restyle(layer){
         let toStyle = layer

         if(toStyle === undefined){
            toStyle = this.drawnItems
         }

         toStyle.setStyle((feature)=>{
            let style = BASE_STYLE
            style.color = colorGradient(
               (feature.properties.intensity)/this.nchoices, COLORS.low, COLORS.high
            )
            style.fillOpacity = ((feature.properties.confidence/100)*0.5) + 0.2
            if(feature.properties.selected !== undefined){
               style.opacity = 0.9 
               style.weight = 9
            } else {
               style.weight = 2
            }
            return style
         })

      },

      computeStyle: function(layer){
         let base = {
            color: colorGradient((layer.feature.properties.intensity)/5,COLORS.low,COLORS.high), 
            fillOpacity: 0.4+((layer.feature.properties.confidence / 100)*0.4)
         }
         if(layer.url == this.infocus){
            base.weight = 5
         } else {
            base.weight = 0.1
         }
         return base
      },

      non_answer(){
         this.$api.post.rel(`nonanswer/${this.$route.params.gwno}`)
            .then(()=>{
               this.$router.push("/")
            })
            .catch((e)=>{
               console.error(e)
            })

      }
   }
}
</script>
