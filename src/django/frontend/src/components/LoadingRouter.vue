<!--
This component is responsible for conditional routing of the user,
based on their current participation status. The routing follows a
hand-holding strategy designed to maximize participation.
-->
<template>
<Card>
</Card>
</template>
<script>
import Card from "@/components/Card"

export default {
   components: {Card},

   data(){
      return {
         status: "Doing some stuff"
      }
   },

   methods:{
      check_open(was_open,was_closed){
         this.$api.get.rel("period/open")
            .then((r)=>{
               if(r.data.open){
                  was_open()
               } else {
                  was_closed()
               }
            })
      },

      check_informed(callback){
         if(!this.$cookies.get("informed")){
            this.$router.push("/info")
         } else {
            if(callback!==undefined){
               callback()
            }
         }
      },

      check_assigned(callback){
         this.$api.get.rel("profile/assigned")
            .then((assigned_countries)=>{
               if(assigned_countries.data.countries.length == 0){
                  this.$router.push("/assign")
               } else {
                  if(callback!==undefined){
                     callback()
                  }
            }})
      },
      check_fulfilled(callback){
         this.$api.get.rel("profile/unfulfilled")
            .then((unfulfilled)=>{
               if(unfulfilled.data.countries.length>0){
                  this.$router.push("/progress")
               } else {
                  if(callback!==undefined){
                     callback()
                  }
               }
            })
      },
      check_metadata(callback){
         this.$api.get.rel("profile/exists")
            .then((profile)=>{
               let hasmeta = profile.data.profile
               if(!hasmeta){
                  this.$router.push("/questionaire")
               } else {
                  if(callback!==undefined){
                     callback()
                  }
               }
            })
      }
   },

   mounted(){
      // This is ugly, but it works!
      this.check_informed(()=>{
         this.check_open(
         // Was open
            ()=>{
               this.check_assigned(()=>{
                  this.check_fulfilled(()=>{
                     this.check_metadata(()=>{
                        this.$router.push("/status")
                     })
                  })
               })
            },
         // Was closed 
            ()=>{
               this.check_metadata(()=>{
                  this.$router.push("/menu")
               })
            }
         )
      })
   }
}
</script>
