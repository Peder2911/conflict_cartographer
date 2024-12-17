<template>
   <div id="root">
      <div id="content" v-if="loaded">
         Currently predicting for
         <div class="year">{{ cyear }} - Q{{ cquarter }}</div>
         <div class="months">{{ cmonths }}</div>
         <div id="bwrapper">
            <div id="ball">
               <div class="quarter" id="q1" :class="{'current': q==4}"></div>
               <div class="quarter" id="q2" :class="{'current': q==1}"></div>
               <div class="quarter" id="q3" :class="{'current': q==2}"></div>
               <div class="quarter" id="q4" :class="{'current': q==3}"></div>
            </div>
         </div>
      </div>
      <Spinner v-else/>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

#root
   display: grid
   place-items: center
   background: $ui-panelgray
   padding: $menu-gaps
   border-radius: $roundedness
   font-size: 18px

#content
   display: grid
   place-items: center


#ball
   display: grid
   grid-template-areas: "q2 q3" "q1 q4"
   grid-gap: 2px 
   height: 100px 
   width: 100px 
   clip-path: circle(50px at center)

.quarter
   display: grid
   place-items: center
   background: $ui-darkgray

.quarter.current
   background: $ui-highlight

#q1
   grid-area: q1
#q2
   grid-area: q2
#q3
   grid-area: q3
#q4
   grid-area: q4

</style>
<script>
import Spinner from "@/components/Spinner"

export default {
   name: "Calendar",
   components: {
      Spinner
   },
   computed: {
      cyear() {
         return this.q < 4 ? this.year : this.year+1
      },
      cquarter() {
         return this.q < 4 ? this.q+1 : 1
      },
      cmonths(){
         switch(this.q){
            case 1: 
               return "Apr May Jun"
            case 2: 
               return "Jul Aug Sept"
            case 3: 
               return "Oct Nov Dec"
            case 4: 
               return "Jan Feb Mar"
            default:
               return ""
         }
      }
   },
   data(){
      return {
         year: 2020,
         q: 4,
         loaded: false
      }
   },
   mounted(){
      this.$api.get.rel("calendar")
         .then((r)=>{
            let d = r.data
            this.year = d.year
            this.q = d.quarter
            this.loaded = true
         })
         .catch((e)=>{
            console.error(e)
         })
   }
}
</script>
