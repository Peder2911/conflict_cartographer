<template>
<div class="container">
   <div class="card" v-if="loaded">
      <div v-html="waiver"/>
      <button v-on:click="agree">I consent</button>
   </div>
   <Spinner v-else>{{ error }}</Spinner>
</div>
</template>

<style lang="sass" scoped>
@import "@/sass/variables"

.container
   display: grid
   place-items: center
   height: 100%
   width: 100%

.card
   display: grid
   justify-items: center
   background: $ui-background
   border-radius: $roundedness
   padding: 0px 50px 50px 50px
   margin-top: 50px
</style>

<script>
import Spinner from "@/components/Spinner"

export default {
   name: "Waiver",
   data(){
      return {
         loaded: false,
         error: "",
         waiver: ""
      }
   },
   components: {
      Spinner
   },
   methods: {
      agree(){
         this.$api.post.rel("waiver",{data:{"agree":true}})
            .then(()=>{
               window.location.reload()
            })
            .error((e)=>{
               this.error = e
            })
      }
   },

   mounted(){
      this.$api.get.rel("waiver")
         .then((r)=>{
            this.loaded = true
            this.waiver = r.data.message
         })
         .catch((e)=>{
            this.error = e
         })
   }
}
</script>


