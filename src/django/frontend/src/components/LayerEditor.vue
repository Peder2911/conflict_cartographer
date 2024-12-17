<template>
   <div class="root">
      <div class="inputcard">
         <h2>Intensity</h2>
         <div class="intensity-input" v-for="choice in choices" :key="choice.key">
            <input type="radio" v-model="layer.feature.properties.intensity" :value="choice.value">
            <label class="cat-label" :for="choice.key">{{ choice.key }} casualties</label>
         </div>
      </div>
      <div class="inputcard">
         <h2>Confidence</h2>
         <vue-slider 
            v-model="layer.feature.properties.confidence"
            :min="0"
            :max="100"
            :interval="1"
            >
         </vue-slider>
      </div>
   </div>
</template>
<style lang="sass" scoped>

@import "@/sass/variables"

.cat-label
   font-size: 18px
   font-weight: bold
   line-height: 25px

h2
   margin: 0

.inputcard
   background: #f0f0f0 
   padding: 20px
</style>
<script>

import VueSlider from "vue-slider-component"
import "vue-slider-component/theme/default.css"
import "@/sass/vueslider.sass"

export default {
   components:{VueSlider},
   data(){
      return {
         choices: [
            {key:"Low (1-25)",value:0},
            {key:"Medium (26-99)",value:1},
            {key:"High (>100)",value:2},
         ],
      }
   },
   props: ["layer"],
}
</script>
