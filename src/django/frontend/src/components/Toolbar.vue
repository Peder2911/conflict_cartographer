<template>
   <div id="toolbarContainer">
      <div></div>
      <div id="toolbar">
         <h1>Drawn areas:</h1>
         <div v-for="layer in layers" v-bind:key="layer.url">
            <layer-view 
               v-on:mouseover = "focusOn(layer)"
               v-on:onmouseout = "unfocus"
               v-on:deleteMe = "deleteLayer(layer)" 
               v-on:change = "updateLayer(layer)"
               :layer="layer"/>
         </div>
      </div>
   </div>
</template>

<style scoped lang="sass" type="text/css" media="screen">
@import "../sass/variables.sass"
$darken: 0.4

h1
   color: white

div#toolbarContainer
   position: absolute
   top: 0
   right: 0
   display: grid
   grid-template-rows: $menu-el-height $map_height auto
   width: 300px
   margin: 0px

div#toolbar
   overflow-y: scroll
   background: rgba(0,0,0,$darken)
   padding: 0px $menu-gaps 0px $menu-gaps
   margin: 0px

</style>

<script charset="utf-8">
   import LayerView from "./LayerView.vue"

   export default {
      name: "Toolbar",
      props:["layers"],

      methods: {
         deleteLayer: function(layer){
            this.$store.commit("deleteLayer",layer)
         },
         
         updateLayer: function(layer){
            this.$store.commit("updateLayer",layer)
         },

         focusOn: function(layer){
            this.$store.commit("focusOn",layer)
         },

         unfocus: function(){
            this.$store.commit("unfocus")
         },
      },
      components: {
         LayerView 
      },
   }
</script>

