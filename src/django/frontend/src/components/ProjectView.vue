<template>
   <div :class="{'noticeme': !completed}" id="container">
      <div id="actions">
         <div id="drawshapes" class="divbutton" v-on:click="$emit('chosen')">Draw shapes</div>
         <div id="noconflict" class="divbutton" v-on:click="nonanswer" v-if="!hasShapes">No conflict</div>
         <div id="clearshapes" class="divbutton" v-on:click="clear" v-else>Clear shapes</div>
      </div>
      <div id="display">
         <div class="header">
            {{ project.name }}
            <span id="errors">
               {{ errors }}
            </span>
         </div>
         <div id="displaywidgets">
            <CompletedWidget :value="completed"/>
            <Nshapeswidget :value="status.shapes"/>
            <NonanswerWidget :value="status.nonanswer"/>
         </div>
      </div>
      <div class="divbutton" id="deselectButton" v-on:click="deselect">X</div>
   </div>
</template>

<style lang="sass" scoped> 
@import "@/sass/variables"
@import "@/sass/animations"

#errors
   color: red 

#container
   display: grid
   grid-template-columns: $project-menu-card-button-size*2 auto $project-menu-card-button-size 
   grid-gap: $project-menu-card-gaps 
   height: $project-menu-card-height 
   background: $ui-gray
   border-radius: $roundedness
   padding: 0 $project-menu-card-gaps

.noticeme
   animation: nagging 1s infinite

#actions
   display: grid
   margin-bottom: $project-menu-card-gaps
   //grid-template-rows: 1fr
   //grid-gap: $project-menu-card-gaps
   //grid-auto-flow: column

#noconflict:hover
   background: linear-gradient(90deg, $ui-darkgray 0%, $button-blue 100%)

#clearshapes:hover
   background: linear-gradient(90deg, $ui-darkgray 0%, $button-red 100%)

#drawshapes:hover
   background: linear-gradient(90deg, $ui-darkgray 0%, $button-yellow 100%)

.divbutton
   font-size: $project-menu-card-font-size 
   background: $ui-darkgray
   display: grid
   color: white 
   place-items: center
   border-bottom: 4px solid $ui-darkergray
   border-radius: $roundedness
   cursor: pointer
   margin: $project-menu-card-gaps 0
   margin-top: $project-menu-card-gaps - 2px

.divbutton:hover
   filter: brightness(0.9)

#actions > .divbutton
   margin-bottom: 0

#display
   display: grid
   grid-template-rows: 40px auto 
   margin: $project-menu-card-gaps+(-2) 0 

#displaywidgets
   display: flex
   background: $ui-lightgray
   border-radius: $roundedness
   margin-bottom: 2px 
   padding: 0 $project-menu-card-gaps*3

.mockwidget
   background: $ui-highlight
   margin: $project-menu-card-gaps 0 $project-menu-card-gaps $project-menu-card-gaps
   width: 60px
   border-radius: $roundedness

.header
   padding-left: $project-menu-card-gaps
   //background: $ui-lightgray
   border-radius: $roundedness
   font-size: $project-menu-card-font-size 
</style>

<script charset="utf-8">
import CompletedWidget from "@/components/widgets/Completed"
import NonanswerWidget from "@/components/widgets/Nonanswer"
import Nshapeswidget from "@/components/widgets/Nshapes"

export default { name: "ProjectView",
   props: ["project"],
   components: {
      CompletedWidget,
      NonanswerWidget,
      Nshapeswidget
   },
   data(){
      return {
         errors: "",
         loaded: false,
         status: {} 
      }
   },

   computed: {
      completed(){
         return this.status.shapes > 0 || this.status.nonanswer
      },
      hasShapes(){
         return this.status.shapes > 0
      }
   },

   methods: {
      deselect(){
         this.$api.post.rel("editprojects/remove",{data: {"pk":this.project.gwno}})
            .then(()=>{
               this.$emit("deselected")
            })
            .catch((e)=>{
               this.errors = e
         })
      },
      nonanswer(){
         this.$api.post.rel(`nonanswer/${this.project.gwno}`)
            .then(()=>{
               this.$emit("deselected")
            })
            .catch((e)=>{
               this.errors = e
            })
      },
      clear(){
         this.$api.post.rel(`clearshapes/${this.project.gwno}`)
            .then(()=>{
               this.$emit("deselected")
            })
            .catch((e)=>{
               this.errors = e
            })
      }
   },

   mounted(){
      this.$api.get.rel(`projectstatus/${this.project.gwno}`)
         .then((r)=>{
            this.status = r.data
            this.loaded = true
         })
         .catch((e)=>{
            this.errors = e
         })
   }
}
</script>

