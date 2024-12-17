<template>
   <div 
      v-if="show"
      class="modalwrapper">
      <div class="modalmessage">
         <div class="contentwrapper">
            <div v-if="status == 'loaded'">
               <h1>{{ title }}</h1>
               {{ content }}
            </div>
            <div v-else-if="status == 'error'">
               {{ error }}
            </div>
            <div v-else>
               <Spinner/>
            </div>
         </div>
         <div class="closewrapper">
            <button 
               v-on:click="toggle"
               class="closebutton">Close</button>
         </div>
      </div>
   </div>
</template>

<style scoped lang="sass">
.modalwrapper
   position: absolute !important
   overflow: auto !important
   top: 0
   left: 0
   width: 100vw
   height: 100vh
   text-align: center
   background: rgba(0,0,0,0.5)

.modalmessage
   display: inline-block
   margin-top: 5vh 
   padding: 50px
   background: white 
   border-radius: 15px
   font-size: 20px

.contentwrapper
   text-align: left
   height: 75vh 
   width: 50vw 
   overflow: auto

.closebutton
   display: inline-block

</style>

<script charset="utf-8">
import Spinner from "@/components/Spinner"

export default {
   name: "modalmessage",
   components: {
      Spinner
   },

   data(){
      return {
         show: true,
         title:"",
         content: "",
         error: "",
         status: "loading" 
      }
   },
   methods: {
      toggle(){
         this.show = !this.show
         this.$emit("toggle")
      }
   },
   mounted() {
      this.$api.get.rel("currentproject",{"params":{"verbose":true}})
         .then((r)=>{
            this.status = "loaded" 
            this.title = r.data.title
            this.content = r.data.description
         })
         .catch((e)=>{
            this.status = "error"
            this.error = e
         })
   }

}
</script>
