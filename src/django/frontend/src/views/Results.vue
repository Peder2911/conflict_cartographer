<template>
   <Card :loaded="true">
      <template v-slot:header>
         <h1>RESULTS</h1>
      </template>
      <template v-slot:content>
         <div id="content-holder">
            <div id="profile-pic-holder">
               <scale-balance :size="200"></scale-balance>
            </div>
            <div class="results-screen-description">
               <p>
                  Predictions added: {{ added_period_string }}
               </p>
               <p>
                  Period predicted for: {{ pred_period_string }}
               </p>
            </div>
            <div class="summaries">
               <div v-for="c in data" :key="c.gwno" class="summary">
                  <CountrySummary :country="c"></CountrySummary>
                  <button class="continue" v-on:click="$router.push(`/results/${shift}/map/${c.gwno}`)">
                     Details
                     <MapSearchOutline></MapSearchOutline>
                  </button>
               </div>
            </div>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <!--
            <button v-on:click="prevShift">
               <PagePreviousOutline :size=30></PagePreviousOutline>
            </button>
            -->
            <div></div>
            <div class="results-date-container">
               {{ added_period_string }}
            </div>
            <div></div>
            <!--
            <button v-on:click="nextShift">
               <PageNextOutline :size=30></PageNextOutline>
            </button>
            -->
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

#participate-button
   background-color: $ui-highlight

#eval-button
   background-color: $ui-progress-alt

#content-holder
   padding: 0 10px

#profile-pic-holder
   display: grid
   place-items: center

.summary
   border-bottom: 1px solid #666 

.summary:last-of-type
   border-bottom: none

.summary button
   width: 30%
   height: 80px
   margin: 10px 0

.footer-buttons button
   background: $ui-darkgray 

.footer-buttons
   border-top: 1px solid #666
   grid-template-columns: 1fr 3fr 1fr

.results-date-container
   display: grid
   justify-items: center
   font-size: 30px

.results-screen-description
   display: grid
   place-items: center
   font-size: 18px
   line-height: 20px 

.results-screen-description p
   margin: 0

</style>
<script>
import Card from "@/components/Card"
import ScaleBalance from "vue-material-design-icons/ScaleBalance"
import PagePreviousOutline from "vue-material-design-icons/PagePreviousOutline"
import PageNextOutline from "vue-material-design-icons/PageNextOutline"
import MapSearchOutline from "vue-material-design-icons/MapSearchOutline"
import CountrySummary from "@/components/CountrySummary"
import {format_date} from "@/date_formatting"
import * as R from "ramda"

const sort_by_name = R.sortBy(R.prop("foo"))

const mock_country_summary = () => {
   return {
         shapes: Math.round(Math.random()*10),
         conflict_coverage: Math.random()*100, 
         accuracy: Math.random()*100, 
         predicted_area: 800000 + (Math.random()*250000), 
         name: "Somewhere",
   }
}

const date_str = (a,b)=>{
   if(a && b){
      return `${format_date(a,{short:true})} - ${format_date(b,{short:true})}`
   } else {
      return ""
   }
}

export default {
   components: {Card,ScaleBalance,CountrySummary,PagePreviousOutline,PageNextOutline,MapSearchOutline},

   data(){
      return {
         data: [],
         added_period: {},
         pred_period: {},
      }
   },
   methods:{
      prevShift(){
         this.$router.push(`/results/${this.shift-1}`)
      },
      nextShift(){
         this.$router.push(`/results/${this.shift+1}`)
      },
      fetchData(){
         this.data = []
         this.$api.get.rel("eval/countries",{params:{shift:this.shift}})
            .then(async (r)=>{
               let countries = r.data.countries.map((ctry)=>{
                  return this.$api.get.rel(`eval/countries/${ctry.country_id}`,{
                     params: {shift: this.shift}
                     }).then((r)=>{
                        return r.data
                     })
               })
               await Promise.all(countries)
                  .then((ctries)=>{
                     sort_by_name(ctries)
                     this.data = ctries
                  })
            })
         this.$api.get.rel(`period/${this.shift}`)
            .then((r)=>{
               this.added_period = r.data
            })
         this.$api.get.rel(`period/${this.shift+1}`)
            .then((r)=>{
               this.pred_period = r.data
            })
      }
   },

   computed:{
      shift(){
         return Number.parseInt(this.$route.params.shift)
      },
      added_period_string(){
         return date_str(this.added_period.start,this.added_period.end)
      },
      pred_period_string(){
         return date_str(this.pred_period.start,this.pred_period.end)
      }
   },

   mounted(){this.fetchData()},
   watch:{"$route": "fetchData"}
}
</script>
