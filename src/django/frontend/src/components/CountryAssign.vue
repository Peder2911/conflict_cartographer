<template>
   <Card :loaded="loaded">
      <template v-slot:header>
         <h1>COUNTRIES</h1>
      </template>
      <template v-slot:content>
         <div class="assignments-layout">
            <multiselect 
               v-model="values" 
               :options="options" 
               :searchable="true"
               :close-on-select="false"
               :multiple="true"
               :max-height="500"
               :loading="!loaded"
               selectLabel=""
               deselectLabel=""
               @open="remove_help"
               >
            </multiselect>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-container">
            <button v-on:click="to_router" class="continue">Finished</button>
         </div>
      </template>
      <template v-slot:overlay>
         <div id="help-overlay">
            <p>
               {{ helptext }}
            </p>
         </div>
      </template>
   </Card>
</template>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="sass">
@import "@/sass/variables.sass"

.multiselect__input:hover, .multiselect__single:hover
  border-color: red

.multiselect__option--highlight:after
   background: $ui-gray 
   color: #333

.multiselect__tag
   background: $ui-highlight
   font-size: 20px

.multiselect__tag-icon:hover
   background: $ui-light-highlight

.multiselect__tag-icon
   background: $ui-highlight

.multiselect__tag-icon:after
   background: $ui-highlight !important
   color: white 

input[type=text].multiselect__input
   background: none

.multiselect__option--highlight
   background: $ui-highlight
</style>

<style lang="sass" scoped>

div.assignments-layout
   height: 100%
   margin: 0 10px
   overflow: hidden

div.footer-container
   height: 100%
   width: 100%
   display: grid

button.continue
   margin: 10px

#help-overlay
   display: grid
   width: 100% 
   height: 100% 
   place-items: center
   color: gray
   visibility: hidden 

#help-overlay p
   font-size: 30px
   margin: 20px
   //transform: translate(0,-100px)

@media only screen and (min-height: 600px)
   #help-overlay
      visibility: visible

</style>
<script>
import Card from "@/components/Card"
//import AssignedCountry from "@/components/AssignedCountry"
import Multiselect from "vue-multiselect"
import "@/sass/global.sass"

export default {
   name: "CountryAssign",
   components: {Card,Multiselect},

   data(){
      return {
         countries: [
         ],
         values: [],
         helptext: "Please select the countries you wish to provide predictions for.",
         got_alternatives:false,
         got_assigned:false,
      }
   },

   computed:{
      options(){
         return this.countries.map(c=>c.name)
      },

      loaded(){
         return this.got_alternatives && this.got_assigned
      }
   },
   
   methods: {
      remove_help(){
         this.helptext = "Great! Thanks. Now click the button below to proceed"
      },

      to_router(){
         this.$api.post.rel("profile/assigned",{
            data:{
               selected: this.values 
            }
         })
         .then(()=>{
            this.$router.back()
         })
         .catch((e)=>{
            this.$router.back()
         })
      }
   },

   mounted(){
      this.$api.get.rel("projects")
         .then((r)=>{
            this.countries = r.data.projects
            this.got_alternatives = true
         })
         .catch((e)=>{
            console.error(e)
         })
      this.$api.get.rel("profile/assigned")
         .then((r)=>{
            console.error(r)
            this.values = r.data.countries.map((prj)=>prj.name)
            this.got_assigned = true
         })
         .catch((e)=>{
            console.error(e)
         })
   }
}
</script>
