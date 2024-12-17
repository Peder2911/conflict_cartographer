<template>
   <div class="base">
      <a href="http://www.github.com/peder2911">
         <img :src="logo" alt="Peder G. Landsverk">
      </a>
   </div>
</template>

<script>
import logo from "../images/landsverk_small.png"
export default {
   data() {
      return {
         logo: logo
      }
   }
}

</script>

<style scoped lang="sass"> 
.base
   position: absolute 
   top: 0
   right: 0
   height: 50px

img
   max-height: 100%
   max-width: 100%
   margin: 12px

</style>
