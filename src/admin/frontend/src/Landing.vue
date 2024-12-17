<template>
   <div id="root">
      <side-bar>
         Landing
      </side-bar>
   </div>
</template>

<style>
html, body {
   padding: 0;
   margin: 0;
}
</style>

<style scoped lang="sass">
@import "/sass/variables.sass"

#root
   height: 100%
   display: grid
   grid-template-columns: $sidebar-size auto
</style>

<script lang="js">
import SideBar from "/components/SideBar.vue"

export default {
   name: "landing",
   components: {SideBar},
   mounted(){
      console.log("foo")
   }
}
</script>
