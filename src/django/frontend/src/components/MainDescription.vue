<template>
   <div id="project-description">
      <h1>{{ title }}</h1>
      <p class="bullet">•</p>
      <p v-html="description"></p>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables.sass"
h1
   font-size: 26px
   text-align: center

#project-description
   padding: $menu-gaps 
   min-height: 0px
   background: $ui-panelgray
   border-radius: $roundedness
   font-size: 16px 

p.bullet
   text-align: center
   font-size: 40px 
   line-height: 16px
   color: #c0c0c0

</style>
<script>
export default {
   name: "MainDescription",
   data(){
      return {
         title: "",
         description: ""
      }
   },
   mounted(){
      this.$api.get.rel("currentproject")
         .then((r)=>{
            this.title = r.data.title
            this.description = r.data.description
         })
         .catch((e)=>{
            console.error(e)
            this.title = "Error"
            this.description = "Error fetching project description.".repeat(20)
         })
   }
}
</script>
