<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h1>NEXT UP</h1>
      </template>

      <template v-slot:content>
         <div id="status-menu">
            <div id="status-nextup">
               <div v-if="next !== undefined" id="status-nextup-overlay">
                  <h2>Conflict intensity predictions for</h2>
                  <h1>{{ next.name }}</h1>
                  <h2 v-if="pred_start!==undefined">Between {{ pred_start }} and {{ pred_end }}</h2>
               </div>
               <div id="plot">
               </div>
            </div>
            <div id="status-other">
               <CountryStatusTable v-if="assigned.length>0" :countries="assigned">
               </CountryStatusTable>
            </div>
         </div>
      </template>

      <template v-slot:footer>
         <div class="footer-buttons">
            <button title="Add predictions for next country"
               v-on:click="go_to_next" class="continue">Add predictions for {{ next? next.name : ""}}</button>
         </div>
      </template>

   </Card>
</template>

<style lang="sass" scoped>

@import "@/sass/variables"

#status-menu
   display: grid
   grid-template-rows: auto 1fr 
   justify-items: center
   width: 100%
   height: 90%

#status-menu>div
   width: 100%

#status-nextup
   display: grid
   place-items: center
   background: $ui-highlight 
   padding: 10px 0 
   position: relative

#status-nextup-overlay h2
   color: white

#status-nextup-overlay
   position: absolute
   top: 0
   left: 0
   width: 100%
   height: 100%
   display: grid
   grid-template-rows: 1fr 6fr 1fr
   place-items: center
   color: #333
   z-index: 999

#plot
   height: 420px
   width: 420px 
   cursor: default

#status-other
   padding: 20px

#status-other table
   width: 100%

.list-category
   display: grid
   grid-template-rows: 1fr 1fr

.hlist>div
   margin: 0 $menu-gaps/2
   width: 40px
   display: inline-block
   background: $ui-highlight 
   padding: 4px
   font-weight: bold
   color: white

.hlist
   overflow-x: auto
   overflow-y: hidden
   white-space: nowrap
   //background: #ddd
   border-radius: 2px
   padding: 10px 10px

</style>

<style>
.leaflet-container {
    background: none;
    outline: 0;
}
</style>

<script>
import Card from "@/components/Card"
import CountryStatusTable from "@/components/CountryStatusTable"
import L from "leaflet"
import "leaflet/dist/leaflet.css"
import {shape_to_latlng_box} from "@/configure_map"
import {format_date} from "@/date_formatting"

export default {
   components: {Card,CountryStatusTable},
   data(){
      return {
         next: undefined,
         //pending: [],
         //fulfilled: [],
         loaded: false,
         pred_start:undefined,
         pred_end:undefined,
         assigned: [],
      }
   },

   computed:{
      all(){
         let all = this.pending.concat(this.fulfilled)
         if(this.next !== undefined){
            all = all.concat([this.next])
         }
         return all
      }
   },

   methods:{
      go_to_next(){
         this.$router.push(`/ctry/${this.next.gwno}`)
      },
      go_to_assign(){
         this.$router.push("/assign")
      }
   },

   mounted(){
      let map = new L.Map("plot")

      map.zoomControl.remove()
      map.attributionControl.remove()
      map.dragging.disable();
      map.touchZoom.disable();
      map.doubleClickZoom.disable();
      map.scrollWheelZoom.disable();
      map.boxZoom.disable();
      map.keyboard.disable();

      this.$api.get.rel("profile/next")
         .then((rsp)=>{
            if(rsp.data.status != "active"){
               this.$router.push("/")
            } else {
               this.next = rsp.data.next
               let bbox = shape_to_latlng_box(this.next.shape).pad(.1)
               map.fitBounds(bbox)

               let layer = L.geoJson(this.next.shape,{
                  style:{
                     color: "white",
                     opacity: 1,
                     fillOpacity: 1

                  }
               })

               layer.addTo(map)
               this.loaded = true

               this.$api.get.rel("period/next")
                  .then((r)=>{
                     this.pred_start = format_date(r.data.start)
                     this.pred_end = format_date(r.data.end)
                  })

               this.$api.get.rel("profile/assigned")
                  .then((r)=>{
                     this.assigned = r.data.countries.filter((ctry)=>{
                        return ctry.gwno !== this.next.gwno
                     })
                  })
            }
         })
   }
}
</script>
