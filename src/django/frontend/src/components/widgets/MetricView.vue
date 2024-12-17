
<template>
   <div class="metric-view-container">
      <div class="title">
         <slot>
         </slot>
         <span>
            {{ title }}
         </span>
      </div>
      <div class="figures">
         <div :style="{fontSize: height}" class="percentage">
            {{ current_rounded }} 
            {{ percentage? "%":"" }}
         </div>
         <div class="progress">
            <ChevronUp v-if="progress_increase" :size=40 fillColor="green"></ChevronUp>
            <ChevronDown v-else :size=40 fillColor="red"></ChevronDown>
         </div>
      </div>
   </div>
</template>

<style lang="sass" scoped>

.figures
   display: grid
   grid-template-columns: 2fr 1fr 1fr 
   align-items: center
   height: 100%

.percentage
   font-size: 80px
   line-height: 50px

.material-design-icon
   height: 100%

.title span
   display: inline-block
   font-size: 20px
   vertical-align: middle 
   line-height: normal

.metric-view-container
   margin: 30px 0

</style>

<script>
import ChevronUp from "vue-material-design-icons/ChevronUp"
import ChevronDown from "vue-material-design-icons/ChevronDown"

export default {
   components: {ChevronUp,ChevronDown},

   props: {
      title: String,
      current: Number,
      previous: Number,
      roundTo: {
         type: Number,
         default: 1,
      },
      height: {
         type: String,
         default: "50px",
      },
      percentage: {
         type: Boolean,
         default: true
      }
   },
   computed: {
      progress_increase(){
         return this.current >= this.previous
      },
      current_rounded(){
         let factor = Math.pow(10,this.roundTo)
         return Math.round(this.current*factor) / factor 
      }
   }
}
</script>
