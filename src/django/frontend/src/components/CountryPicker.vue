<template>
   <div id="root">
      <div id="selectHolder" v-if="active">
         <div id="boxHolder">
            <p class="label">Country:</p>
            <select id="selectbox" name="country" v-model="selected">
               <option v-for="c in choices" :value="c.pk" :key="c.pk">{{c.name}}</option>
            </select>
         </div>
         <div id="dispatch" class="divbutton" v-on:click="dispatch">Add</div>
         <div id="close" class="divbutton" v-on:click="active = false">X</div>
      </div>
      <button id="addProjects" v-if="!active" v-on:click="activate">Add country +</button>
   </div>
</template>
<style lang="sass" scoped>
@import "@/sass/variables.sass"

#root
   display: grid
   width: 100%

button#addProjects
   border: none
   height: $project-menu-card-height 
   display: grid
   place-items: center
   font-size: 30px
   line-height: 0
   color: $ui-darkgray
   background: $ui-lightgray 

button#addProjects:hover
   color: $ui-highlight

#boxHolder
   display: grid
   grid-template-rows: 1fr 2fr

#selectHolder
   display: grid
   place-items: center
   grid-gap: $project-menu-card-gaps 
   grid-template-columns: auto $project-menu-card-button-size $project-menu-card-button-size 
   height: $project-menu-card-height
   background: $ui-lightgray
   border-radius: $roundedness
   padding: 0 $project-menu-card-gaps

#selectHolder > *
   height: 100px 
   width: 100%

p.label
   font-size: 28px
   margin: 0
   margin-left: $menu-gaps

#selectbox
   padding-left: $menu-gaps

.divbutton
   background: $ui-darkgray
   border-radius: $roundedness
   border-bottom: 4px solid $ui-darkergray
   display: grid
   place-items: center
   font-size: $project-menu-card-font-size 

.divbutton:hover
   background: $ui-highlight 
   cursor: pointer

select
   background: $ui-gray
   font-size: $project-menu-card-font-size 
   padding: 0
   height: 100%

select:focus
   border: 1px solid $ui-highlight

</style>
<script>

export default {
   name: "CountryPicker",
   data(){
      return {
         active: false,
         choices: [],
         selected: {} 
      }
   },
   methods: {
      activate(){
         this.choices = this.$api.get.rel("projectchoices")
            .then((r)=>{
               this.choices = r.data.projects
               this.choices = this.choices.sort((a,b)=>{
                  let ta = a.name.toUpperCase()
                  let tb = b.name.toUpperCase()
                  return (ta < tb) ? -1 : (ta > tb) ? 1 : 0
               })
               this.selected = this.choices[0]
               this.active=true
            })
            .catch((e)=>{
               console.error(e)
               this.active=false
            })
      },
      dispatch(){
         this.active = false
         this.$api.post.rel("editprojects/add",{data:{"pk":this.selected}})
            .then(()=>{
               this.$emit("addedProject")
               })
            .catch((e)=>{
               console.error(e)
            })
      }
   }
}
</script>
