<template>
   <Card :loaded="true">
      <template v-slot:header>
         <h1>Delete profile</h1>
      </template>
      <template v-slot:content>
         <div id="content-root">
            <div>
               <alert-octagram :size="300" fillColor="orange"></alert-octagram>
               <p>Profile deletion removes your personal information from the app, and fully anonymizes your previously submitted predictions.</p>
               <p>By deleting your profile, you opt out of any future evaluation rounds, and you will not be able to log back in.</p>
            </div>
         </div>
      </template>
      <template v-slot:footer>
         <div class="footer-buttons">
            <button class="continue" v-on:click="deleteme">I understand, delete my profile.</button>
            <button class="alt" v-on:click="$router.back()">No, go back!</button>
         </div>
      </template>
   </Card>
</template>
<script>
import Card from "@/components/Card"
import AlertOctagram from "vue-material-design-icons/AlertOctagram"
export default {
   components: {Card, AlertOctagram},
   methods: {
      deleteme(){
         this.$api.get.rel("profile/deleteme")
            .then(()=>{
               window.location.href = "/accounts/login"
            })
            .catch((e)=>{

            })
      }
   }
}
</script>
<style lang="sass" scoped>
#content-root
   display: grid
   place-items: center
   height: 100%
   margin: 0 50px

#content-root>div
   display: grid
   place-items: center

</style>
