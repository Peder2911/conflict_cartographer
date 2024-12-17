<template>
   <div class="root">
      <div class="holder">
         <div class="content-wrapper">
            {{country.iso2c}}
         </div>
      </div>
   </div>
</template>
<style lang="sass" scoped>
.root
   //height: 100%
   width: 100% 

.holder
   position: relative
   width: 100% 
   padding-top: 56.25%
   background: red

.content-wrapper
   position: absolute
   top: 0
   left: 0
   display: grid
   place-items: center
   height: 100%
   width: 100%
   font-size: 30px

</style>
<script>

export default {
   name: "CountryView",
   props: ["country"],
}
</script>
