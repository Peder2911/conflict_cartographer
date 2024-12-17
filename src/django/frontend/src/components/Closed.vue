<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h2>CLOSED</h2>
      </template>
      <template v-slot:content>
         <div id="closed-message-container">
            <div id="closed-message-box">
               <map-clock-outline :size="200"></map-clock-outline>
               <p>
                  We are not currently accepting predictions. The next round
                  of predictions can be submitted between
               </p>
               <p id="closed-opening-date">
                  <span class="date">{{opening_date}}</span>  
                  and 
                  <span class="date">{{closing_date}}</span>  
               </p>
               <p>
                  Please come again in {{ days_until_open }} days!
               </p>
            </div>
         </div>
      </template>
      <template v-slot:footer></template>
   </Card>
</template>

<style lang="sass" scoped>
@import "@/sass/variables"

#closed-message-container
   height: 100%
   width: 100%
   display: grid
   place-items: center
#closed-message-box
   display: grid
   justify-items: center

#closed-message-box>p
   width: 75%
   text-align: center

#closed-opening-date
   font-size: 18px

#closed-opening-date .date
   color: $ui-highlight
   font-weight: bold

</style>

<script>
import Card from "@/components/Card"
import MapClockOutline from "vue-material-design-icons/MapClockOutline"
export default {
   components: {Card,MapClockOutline},
   data(){
      return {
         opening_date:null,
         closing_date:null,
         days_until_open:null,
      }
   },
   computed:{
      loaded(){
         return this.opening_date!==null &&
            this.closing_date!==null &&
            this.days_until_open!==null
      }
   },
   mounted(){
      this.$api.get.rel("period/open")
         .then((r)=>{
            this.opening_date= r.data.opening_date
            this.closing_date = r.data.closing_date
            this.days_until_open = r.data.days_until_open
         })

   }
}
</script>
