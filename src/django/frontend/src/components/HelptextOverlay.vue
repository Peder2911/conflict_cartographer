<template>
   <div class="overlay helptext-overlay">
      <div class="helptext">
         <div>
            <slot></slot>
         </div>
      </div>
      <div class="viewport"></div>
   </div>
</template>
<style lang="sass">
@import "@/sass/variables.sass"
.helptext h1
   margin-bottom: 0

.helptext
   height: 100%
   width: 90%
   padding: 30px 60px
   font-size: 25px

.helptext-overlay
   display: grid
   grid-auto-flow: rows 
   grid-template-rows: $tray-size * 2 auto
   grid-template-columns: 1fr 
   place-items: center

@media only screen and (min-width: $mob-width)
   .helptext-overlay
      grid-auto-flow: columns
      grid-template-columns: 700px 1fr 
      grid-template-rows: 1fr

   .helptext
      display: grid
      padding-top: 70px
      font-size: 30px

</style>
<script>
</script>
