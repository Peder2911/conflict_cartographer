<template>
   <Card :loaded="loaded">
      <template v-slot:header><h1>PROJECT INFO</h1></template>
      <template v-slot:content>
         <div id="project-info-text">
            <h2> {{ title.toUpperCase() }} </h2>
            <p>
               {{ body }}
            </p>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button title="Continue"
               v-on:click="go_to_router" class="continue">Proceed</button>
         </div>
      </template>
   </Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

#project-info-text
   padding: 20px
   white-space: pre-wrap

#project-info-text>h2
   color: $ui-highlight 
   margin-top: 0

</style>
<script>
import Card from "@/components/Card"
export default {
   components:{Card},
   data(){
      return {
         title: "",
         body: "",
         loaded: false 
      }
   },
   mounted(){
      this.$api.get.rel("info/verbose")
         .then((r)=>{
            this.title = r.data.title
            this.body = r.data.description
            this.loaded = true
         })
         .catch((e)=>{
            console.error(`Error getting info: ${e}`)
         })
   },
   methods:{
      go_to_router(){
         this.$cookies.set("informed",true)
         this.$router.back()
      }
   },
}
</script>
