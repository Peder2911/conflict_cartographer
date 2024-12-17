<template>
   <div id="results-map-root">
      <div id="map-element"></div>
      <div id="map-overlay">
         <div class="overlay-container">
            <div class="header">
               <button class="back-button" v-on:click="$router.go(-1)">Back</button>
               <select v-model="metric_name">
                  <option value="coverage">Coverage</option>
                  <option value="accuracy">Accuracy</option>
               </select>
            </div>
            <div class="viewport"></div>
            <div class="footer">
               <div class="footer-metrics">
                  <div class="hero"> 
                     <div class="figure">
                        {{ metric_summary }}
                     </div>
                     <div class="title">
                        {{ metric_summary? metric_name:"" }}
                     </div>
                  </div>
                  <div class="stats">
                     <table>
                        <tr v-for="s in stats" :key="s.name">
                           <td>{{s.name}}:</td>
                           <td>{{s.value}}</td>
                        </tr>
                     </table>
                  </div>
               </div>
            </div>
         </div>
         <transition name="fade">
            <div v-if="!loaded" id="loading-cover" class="overlay">
               <Spinner v-if="!loaded"></Spinner>
            </div>
         </transition>
      </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

h1
   line-height: 50px 

#results-map-root
   height: 100vh
   width: 100vw
   position: relative

#map-element
   height: 100vh
   
#map-overlay
   pointer-events: none
   position: absolute
   top: 0
   left: 0
   height: 100vh
   width: 100vw
   //background: rgba(0,255,0,0.2) 
   z-index: 9999
   display: grid
   place-items: center

.header
   display: grid
   grid-template-columns: 1fr 2fr 
   grid-gap: $menu-gaps
   place-items: center
   pointer-events: auto
   border: none

.header button
   height: 60px
   width: 100%
   background-color: $ui-darkgray
   color: white 

.footer
   display: grid
   place-items: center

.footer>div>div
   display: inline-block
   pointer-events: auto

.stats table
   width: 100% 
   background: none
   font-size: 20px

.overlay-container
   height: 100%
   display: grid
   width: 100%
   max-width: 800px
   min-width: 500px
   grid-template-rows: 100px auto 220px

.stats table td, h1, .hero
   background: $ui-darkergray
   color: white
   padding: 8px 10px
   border-radius: 3px

.hero
   background: $ui-highlight
   border-radius: 8px

.hero .figure
   font-size: 90px

select
   width: 100%
   height: 50%
   font-size: 30px
   border-radius: 5px

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

</style>
<script>
import * as L from "leaflet"
import {TILE_URL,ll_gj_box} from "@/configure_map"
import bbox from "geojson-bbox"
import {ged_point} from "@/map"
import {display_functions,compute_stats} from "@/results_display"
import {round_to} from "@/util"
import Spinner from "@/components/Spinner"

function fetch_country(map,api,gwno){
   return api.get.rel(`countries/${gwno}`)
      .then((r)=>{
         new L.TileLayer.BoundaryCanvas(TILE_URL,{
            boundary: r.data.shape,
            id: "countrytiles",
            opacity: 0.9
         }).addTo(map)

         map.fitBounds(ll_gj_box(r.data.shape))
      })
}

function fetch_ged(api,gwno,shift){
   let pts = api.get.rel(`eval/ged/points/${gwno}/${shift+1}`)
   let buf = api.get.rel(`eval/ged/buffered/${gwno}/${shift+1}`)
   return pts.then(async (points)=>{
      return buf
         .then((buffered)=>{
            return {
               points: points.data,
               buffered: buffered.data
            }
         })
   })
}

function fetch_predictions(api,gwno,shift){
   return api.get.rel(`eval/countries/${gwno}/preds/${shift}`)
      .then(async d => {
         d.data.features = await Promise.all(d.data.features.map(async ftr=>{
            await api.get.rel(`eval/preds/${ftr.id}`)
               .then((r)=>{
                  ftr.properties = r.data.properties
               })
            return ftr
         }))
         return d
      })
}

async function fetch_data(map,api,gwno,shift){
   let points,buffered,predictions

   let f = fetch_ged(api,gwno,shift)
      .then((data)=>{
         points = L.geoJSON(data.points)
         buffered = L.geoJSON(data.buffered)
      })
      
   let r = fetch_predictions(api,gwno,shift)
      .then((r)=>{
         predictions = L.geoJSON(r.data)
      })
   await Promise.all([f,r])

   return {
      points: points,
      buffered: buffered,
      predictions: predictions
   }
}

function style_data(metric_name,data,map){
   let fn_set = display_functions[metric_name]
   Object.keys(data).forEach(lyr_name=>{
      let fn = fn_set[lyr_name]
      if(fn !== null){
         data[lyr_name] = fn(data[lyr_name],map)
      } else {
         data[lyr_name] = null
      }
   })
   return data
}

function add_layers(data,map){
   map.eachLayer(lyr=>{
      if(!(lyr instanceof L.TileLayer)){
         map.removeLayer(lyr)
      }
   })

   let seq = ["predictions","buffered","points"]
   Object.entries(data).forEach(entry=>{
      if(entry[1] !== null){
         map.addLayer(entry[1])
      }
   })
   seq.forEach(name=>{
      if(data[name] !== null){
         data[name].bringToFront()
      }
   })
}

let cached_data, cached_for
async function update_data(map,api,gwno,shift,metric_name){
   let data
   if(cached_data === undefined | cached_for != gwno){
      data = fetch_data(map,api,gwno,shift)
   } else {
      data = Promise.resolve({...cached_data})
   }
   return data.then((d)=>{
            cached_data = {...d}
            cached_for = gwno
            add_layers(style_data(metric_name,d,map),map)
            return compute_stats(metric_name,d)
         })
}

export default {
   components: {Spinner},
   data(){
      return {
         map: undefined,
         country: undefined,
         ged_points: undefined,
         ged_buffered: undefined,
         stats: [],
         metric_summary: "",
         metric_name: "accuracy",
         loaded: false
      }
   },

   computed: {
      shift(){
         return Number.parseInt(this.$route.params.shift)
      },
      gwno(){
         return Number.parseInt(this.$route.params.gwno)
      },
   },

   mounted(){
      let map = L.map("map-element")
      this.map = map

      L.tileLayer(TILE_URL,{
         id: "background",
         ext: "png",
         opacity: 0.8
      }).addTo(map)

      fetch_country(map,this.$api,this.gwno)

      update_data(map,this.$api,this.gwno,this.shift,this.metric_name)
         .then((stats)=>{
            this.stats = stats.list 
            this.metric_summary = stats.hero
            this.loaded = true
         })
   },
   watch:{
      metric_name(){
         update_data(this.map,this.$api,this.gwno,this.shift,this.metric_name)
            .then((stats)=>{
               this.stats = stats.list 
               this.metric_summary = stats.hero
            })
         }
   }
}
</script>
