<template>
<Card :loaded="true">
   <template v-slot:header>
      <h1>PROFILE INFORMATION</h1>
   </template>
   <template v-slot:content>
      <div id="content-root">
         <div id="prompt">
            <p>Please add some details about yourself</p>
         </div>
         <div id="questions">
            <Question v-for="question in questions" :question="question" :key="question.label"></Question>
         </div>
      </div>
   </template>
   <template v-slot:footer>
      <div class="footer-buttons">
         <button title="Submit profile information"
            v-on:click="to_router" class="continue">Submit</button>
         <button title="Skip profile questionaire"
            v-on:click="skip" class="alt">Skip</button>
      </div>
   </template>
</Card>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"
@import "@/sass/global"

#content-root
   display: grid
   grid-template-rows: 100px auto
   height: 100%
   padding: 10px

</style>

<script>
import Card from "@/components/Card"
import Question from "@/components/Question"

const QUESTIONS = [
   {
      "title":"profession",
      "label": "Profession",
      "description":"What is your current profession?",
      "value":"",
   },
   {
      "title":"affiliation",
      "label": "Affiliation",
      "description":"What is your institutional affiliation?",
      "value":"",
   },
]

export default {
   data(){
      return {
         questions: QUESTIONS
      }
   },
   methods: {
      to_router(){
         // Post metadata to API
         this.$api.post.rel("profile/meta",{
            data: this.questions
         })
         .then(()=>{
            this.$router.back()
         })
         .catch((e)=>{
            console.error(e)
         })
      },
      skip(){
         this.$api.post.rel("profile/meta",{
               data: [
                  {"title":"skipped","value":"true"}
               ]
            })
         .then(()=>{
            this.$router.back()
         })
         .catch((e)=>{
            console.error(e)
         })
      }
   },
   components: {Card,Question}
}
</script>
