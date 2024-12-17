<template>
   <div class="sbwidget">
      <button class="closed" id="activatebutton" v-if="mode=='inactive'" v-on:click="toggle">
         Give us some feedback!
      </button>
      <div class="open form" v-if="mode=='active'">
         <!--<div class="label">Feedback text</div>-->
         <label>Feedback text</label>
         <textarea v-model="feedback"/>
         <label>Star rating: {{ stars }}</label>
         <div id="stars">
            <input v-model="stars" value=1 type="radio">
            <input v-model="stars" value=2 type="radio">
            <input v-model="stars" value=3 type="radio">
            <input v-model="stars" value=4 type="radio">
            <input v-model="stars" value=5 type="radio">
         </div>
         <button v-on:click="submit">Submit</button>
         <div class="closebutton" v-on:click="toggle">X</div>
      </div>
      <div class="thanks" v-if="mode=='thanks'">
         {{ msg }}
      </div>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"
@import "@/sass/sidebarwidget"
@import "@/sass/generic"

#form>textarea
   height: 100%
   width: 100%
   margin-bottom: 11px 
   border-top: 2px solid $ui-darkergray 
   border-right: 1px solid $ui-darkergray 
   border-left: 1px solid $ui-darkergray 
   border-radius: $roundedness

#form>button
   width: 100%

#stars
   display: grid
   width: 100%
   height: 28px
   grid-template-columns: repeat(5, 1fr)
   justify-items: center

</style>
<script>
import SbWidget from "@/mixins/SbWidget"

export default {
   name: "Feedback",
   mixins: [SbWidget],
   data(){
      return {
         feedback: "Type your feedback here",
         stars: 3,
      }
   },
   methods: {
      submit(){
         this.$api.post.rel("feedback",{
            data: {
               message: this.feedback,
               stars: this.stars
            }})
            .then(()=>{
               this.toggle()
            })
            .catch((e)=>{
               console.error(e)
            })
      }
   }
}
</script>
