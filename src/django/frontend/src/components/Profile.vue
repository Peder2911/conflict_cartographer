<template>
   <div id="profile-view">
      <div id="profile-centered" v-if="loaded">
            <div id="imgholder">
               <a href="/accounts/profile">
                  <img id="profile-image" :src="img"  alt="">
               </a>
               <div id="exclamation" v-if="noprofile">!</div>
            </div>
         <p id="profile-name">{{this.name}}</p>
      </div>
      <Spinner v-else/>
   </div>
</template>

<style lang="sass" scoped>
@import "@/sass/variables"

#profile-view
   max-height: 300px

#profile-centered
   display: grid
   place-items: center

img#profile-image
   max-height: 100px
   clip-path: circle(50px at center)

#imgholder
   position: relative
#exclamation
   position: absolute
   top: 0
   right: 0
   color: white 
   background: #ff0000 
   width: 20px 
   height: 23px 
   border-radius: 30px
   display: grid
   place-items: center
   font-family: monaco 
   font-size: 15px
   font-weight: bolder 

@keyframes float 
   0%
      transform: translatey(0px)
      background: #ff0000 
   50%
      transform: translatey(-2px)
      background: #ff6666 
   100%
      transform: translatey(0px)
      background: #ff0000 

#exclamation
   animation: float 2s ease-in-out infinite

</style>

<script>
import defaultImage from "@/images/prof.jpg"
import Spinner from "@/components/Spinner"

export default {
   name: "Profile",
   props: ["profile"],
   data() {
      return {
         img: defaultImage,
         hasprofile: false,
         loaded: false
      }
   },

   components: {
      Spinner
   },

   computed: {
      name(){
         return this.profile.name
      },
      noprofile(){
         return ! this.hasprofile
      }
   },

   mounted(){
      this.$api.get.rel("hasprofile")
         .then((r)=>{
            this.hasprofile=r.data.profile 
            this.loaded = true
         })
         .catch((e)=>{
            console.error(e)
         })
   }
}

</script>
