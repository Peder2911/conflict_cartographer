<template>
   <vue100vh class="container">
      <div class="card">
         <div class="overlay loading-cover" :class="{loaded: loaded_with_meta}">
            <Spinner></Spinner>
         </div>
         <div class="holder header">
            <div id="card-header-holder">
               <div id="card-header-nav-title">
                  <button title="Go to home menu"
                     v-on:click="$router.push('/menu')" id="card-header-back-button">
                     <home></home>
                  </button>
                  <div id="card-header-title">
                     <slot name="header"></slot>
                  </div>
                  <button title="Go to project info"
                     v-on:click="$router.push('/info')" id="card-header-help-button">
                     <information></information>
                  </button>
               </div>
               <div id="card-header-profile">
                  <div>
                  </div>
                  <span>
                     {{ username }}
                  </span>
                  <button title="Log out"
                     v-on:click="logout">Log out</button>
               </div>
            </div>
         </div>
         <div id="card-content" class="holder content">
            <slot name="content"></slot>
         </div>
         <div class="holder footer">
            <slot name="footer"></slot>
         </div>
         <div class="overlay">
            <slot name="overlay"></slot>
         </div>
      </div>
   </vue100vh>
</template>
<style lang="sass" scoped>
@import "@/sass/variables"

@keyframes fade
   0%
      opacity: 100% 
   100%
      opacity: 0%
      display: none

.overlay.loading-cover
   background: #aaa 
   height: 100%
   width: 100%
   display: grid
   place-items: center
   z-index: 99999
   pointer-events: none

.overlay.loading-cover.loaded
   animation-name: fade
   animation-duration: 0.5s 
   animation-fill-mode: forwards

.holder
   overflow: hidden

.container
   width: 100vw

.card
   height: 100%
   width: 100%
   display: grid
   grid-template-rows: 85px 1fr 100px 
   position: relative

.content
   overflow-y: auto 

#card-header-holder
   display: grid
   grid-template-rows: 1fr 1fr

#card-header-profile
   display: grid
   grid-template-columns: 60px 1fr 60px
   text-align: center

#card-header-profile>button
   height: 14px 
   color: $ui-darkgray
   background: none
   border: none
   padding: 0
   font-size: inherit 
   margin: 0
   color: $ui-darkergray
   transform: translateX(-10px)

#card-header-nav-title
   display: grid
   grid-template-columns: 60px 1fr  60px

#card-header-nav-title>button
   border: none
   background: none
   color: $ui-darkergray
   //font-size: 18px
   font-weight: bold

#card-header-back-button
   font-size: 30px

#card-header-nav-title>button:hover
   color: $ui-highlight

#card-header-title
   text-align: center

.overlay
   position: absolute 
   top: 0
   left: 0
   height: 100%
   width: 100%
   pointer-events: none

@media only screen and (min-width: $mob-width)
   .card
      width: $mob-width*1.1
      height: 90vh 
      max-height: $mob-height*1.1
      margin: max(20px,4vh) 0
      box-shadow: 0px 3px 5px 2px #eee
      border: 1px solid gray

   .container
      display: grid
      justify-items: center

   .container
      overflow-y: scroll

</style>
<script>
import Spinner from "@/components/Spinner"
import vue100vh from 'vue-100vh'
import Home from "vue-material-design-icons/Home"
import Information from "vue-material-design-icons/Information"

export default {
   name: "Card",
   components:{Spinner,vue100vh,Home,Information},
   props: {
      loaded: {
         type: Boolean,
         default: false,
      }
   },
   data(){
      return {
         username: undefined 
      }
   },
   computed:{
      loaded_with_meta(){
         return this.loaded && this.username !== undefined
      }
   },
   methods:{
      logout(){
         window.location = "/accounts/logout"
      }
   },
   mounted(){
      this.$api.get.rel("profile/whoami")
         .then((r)=>{
            this.username = r.data.name
         })
   }
}
</script>
