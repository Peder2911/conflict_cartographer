<template>
   <vue100vh id="root" class="overlay">
      <div id="slidein-container" :style="box_pos">
         <transition name="slide-fade" mode="out-in">

            <div v-if="hide" id="slidein-hidden" 
               :class="content_class"
               :style="slidein_display" key="hidden">
               <button title="Open slideover"
                  :style="[show_pos,buttons_style]" id="slidein-show-button" v-on:click="hide=false">
                  {{ show_button_text }}
               </button>
            </div>

            <div v-else id="slidein-content"
               :class="content_class" key="visible">
               <div id="hide-holder">
                  <button title="Close slideover"
                    id="slidein-hide-button"
                    :style="[hide_pos,buttons_style]" v-on:click="close">{{ hide_button_text }} </button>
               </div>
               <div id="content-holder">
                  <slot></slot>
               </div>
            </div>

         </transition>
      </div>
   </vue100vh>
</template>
<style lang="sass" scoped>
#slidein-show-button,#slidein-hide-button
   height: 100px 
   width: 100px 
   font-weight: bold
   font-size: 60px !important
   background: rgba(0,0,0,0.1)
   border: none
   color: #222

button:hover
   filter: brightness(3)

#root
   width: 100vw
   overflow: hidden
   z-index: 999

#slidein-content
   pointer-events: auto
   height: 100%
   width: 100%

#slidein-content>div
   height: 100%
   width: 100%
   position: absolute
   top: 0
   left: 0

#hide-holder
   height: 100%
   width: 100%
   display: grid
   place-items: center

#slidein-show-button
   pointer-events: auto

#slidein-hidden
   height: 100%
   width: 100%
   display: grid

.slide-fade-enter-active 
  transition: all .3s ease

.slide-fade-leave-active
  transition: all .2s cubic-bezier(1.0, 0.5, 0.8, 1.0)

.slide-fade-enter, .slide-fade-leave-to
   opacity: 0

.pos-top.slide-fade-enter, .pos-top.slide-fade-leave-to
   transform: translateY(-80px)

.pos-right.slide-fade-enter, .pos-right.slide-fade-leave-to
   transform: translateX(80px)

.pos-bottom.slide-fade-enter, .pos-bottom.slide-fade-leave-to
   transform: translateY(80px)

.pos-left.slide-fade-enter, .pos-left.slide-fade-leave-to
   transform: translateX(-80px)

</style>
<style>
</style>
<script>
import vue100vh from "vue-100vh"
export default {
   name: "Slideover",
   components:{vue100vh},
   props:{
      size: {
         type: Number,
         default: 100,
      },
      direction: {
         type: Number,
         default: 4
      },
      start_open: {
         type: Boolean,
         default: false
      }
   },
   data(){
      return {
         hide: true 
      }
   },
   methods:{
      close(){
         this.hide=true
         this.$emit("was-closed")
      }
   },

   mounted(){
      if(this.start_open){
         this.hide = false
      }
   },

   computed:{
      hide_button_text(){
         switch(this.direction){
            case 1: return "▲"
            case 2: return "►"
            case 3: return "▼"
            case 4: return "◄"
         }
      },
      show_button_text(){
         switch(this.direction){
            case 1: return "▼"
            case 2: return "◄"
            case 3: return "▲"
            case 4: return "►"
         }
      },
      content_class(){
         return {
            "pos-top": this.dir_str=="top",
            "pos-right": this.dir_str=="right",
            "pos-bottom": this.dir_str=="bottom",
            "pos-left": this.dir_str=="left",
         }
      },
      show_pos(){
         return {
         }
      },
      hide_pos(){
         let offset = 100 
         let ud = 0
         let lr = 0
         switch(this.dir_str){
            case "top":
               ud = (this.size / 2)+(offset/2)
               break
            case "bottom":
               ud = -(this.size / 2)-(offset/2)
               break
            case "left":
               lr = (this.size / 2)+(offset/2)
               break
            case "right":
               lr = -(this.size / 2)-(offset/2)
         }
         return {
            transform: `translate(${lr}px, ${ud}px)`,
         }
      },
      box_pos(){
         let left,right,top,bottom

         switch(this.dir_str){
            case "bottom":
               top = "auto" 
               break
            default:
               top = 0 
         }

         switch(this.dir_str){
            case "right":
               right = 0
               break
            default:
               right = "auto" 
         }

         switch(this.dir_str){
            case "bottom":
               bottom = 0 
               break
            default:
               bottom = "auto"
         }

         switch(this.dir_str){
            case "right":
               left = "auto" 
               break
            default:
               left = 0
         }
         return {
            position: "absolute",
            top: top, 
            right: right, 
            bottom: bottom, 
            left: left,
            width: this.width,
            height: this.height,
         }
      },

      slidein_display(){
         let base = {}
         switch(this.dir_str){
            case "top":
            case "bottom":
               base["justify-items"] = "center"
               break
            case "left":
            case "right":
               base["align-items"] = "center"
               break
         }
         switch(this.dir_str){
            case "right":
               base["justify-items"] = "end"
               break
            case "bottom":
               base["align-items"] = "end"
               break
         }
         return base
      },

      box_size(){
         return {
            width: this.width,
            height: this.height,
         }
      },

      dir_str(){
         switch(this.direction){
            case 1: return "top"
            case 2: return "right"
            case 3: return "bottom"
            case 4: return "left"
            default: return "top"
         }
      },
      height(){
         if([1,3].includes(this.direction)){
            return `${this.size}px`
         } else {
            return "100%"
         }
      },
      width(){
         if([2,4].includes(this.direction)){
            return `${this.size}px`
         } else {
            return "100%"
         }
      },
      buttons_style(){
         let br = [0,0,0,0]
         let round 
         switch(this.dir_str){
            case "top": round = [1,2]; break
            case "right": round = [1,4]; break
            case "bottom": round = [3,4]; break
            case "left": round = [1,4]; break
         }
         round.forEach((i)=>{br[i-1] = "20px"})
         let base = {"border-radius": br.join(" ")}
         return base
      },
   },
}
</script>
