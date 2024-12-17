<template>
   <div>
      <div class="country-summary-name">
         <h2>
            {{ country.name }}
         </h2>
      </div>
      <MetricView 
         height="70px"
         title="Coverage"
         :current="country.conflict_coverage*100"
         :previous="country.conflict_coverage*100">
         <SetCenter :size=40></SetCenter>
      </MetricView>
      <MetricView
         height="70px"
         title="Accuracy"
         :current="country.accuracy*100"
         :previous="country.accuracy*100">
         <Bullseye :size=40></Bullseye>
      </MetricView>
   </div>
</template>
<style lang="sass">
@import "@/sass/variables.sass"

h2
   margin-bottom: 0px
   color: $ui-highlight
</style>
<script>
import MetricView from "@/components/widgets/MetricView"
import SetCenter from "vue-material-design-icons/SetCenter"
import Bullseye from "vue-material-design-icons/Bullseye"

export default {
   props: ["country"],
   components: {MetricView,SetCenter,Bullseye},
}
</script>
