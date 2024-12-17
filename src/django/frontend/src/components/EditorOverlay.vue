<template>
   <div class="overlay editor-overlay">
      <div id="editor-overlay-header">
      </div>
      <div id="editor-overlay-viewport">
      </div>
      <div id="editor-overlay-controls">
         <div>
            <button></button>
            <button></button>
            <button></button>
            <button></button>
         </div>
         <div>
            Predicting 1999-2000
         </div>
      </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"


</style>

<script>
export default {
   props: ["mode"],

   data(){
      return {
         value: true 
      }
   },
   methods:{
      go_to_router(){
         this.$router.push("/")
      }
   },
}
</script>
