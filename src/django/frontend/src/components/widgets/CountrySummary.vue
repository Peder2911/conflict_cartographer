<template>
   <tr v-if="loaded">
      <td>
         {{ country.name }}
      </td>
      <td v-if="shapes!==undefined && shapes > 0" class="only-wide">
         <span>{{shapes}} prediction-areas</span>
      </td>
      <td v-else-if="nonanswer" class="only-wide">
         <span>No conflict</span>
      </td>
      <td v-else class="only-wide">
         <span class="noticeme">No prediction</span>
      </td>
      <td>
         <button title="Edit predictions"
            class="continue" v-if="shapes!==undefined" v-on:click="go_to_editor">
            <span v-if="shapes>0">Revise</span>
            <span v-else>Add</span>
         </button>
      </td>
      <td>
         <button title="Clear predictions"
            class="alt" v-on:click="clear">Clear</button>
      </td>
   </tr>
   <tr v-else>
      <td>
         {{ country.name }}
      </td>
   </tr>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

button
   width: 100%
   font-size: 15px
   border-radius: 2px

td
   min-width: 40px

span.noticeme
   color: $ui-highlight

</style>
<script>
export default {
   props: ["country"],
   data(){
      return {
         shapes: undefined,
         nonanswer: false,
         loaded: false
      }
   },
   mounted(){
      this.$api.get.rel(`projects/${this.country.gwno}/status`)
         .then((r)=>{
            this.shapes = r.data.shapes
            this.nonanswer = r.data.nonanswer
            this.loaded = true
         })
         .catch((e)=>{
            console.error(e)
         })
   },
   methods: {
      go_to_editor(){
         this.$router.push(`ctry/${this.country.gwno}`)
      },
      clear(){
         let rq
         if(this.shapes>0){
            rq = this.$api.get.rel(`projects/${this.country.gwno}/clear`)
         } else {
            rq = this.$api.post.rel(`nonanswer/${this.country.gwno}`)
         }
         rq.then(()=>{
               this.$router.push("/")
            })
      },
   }
}
</script>
